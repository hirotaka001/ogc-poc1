# -*- coding: utf-8 -*-
import os
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import slack, const
from src.orion import Orion, OrionError
from src.destination import Destination, DestinationDoesNotExist

logger = getLogger(__name__)


class StartReceptionAPI(MethodView):
    NAME = 'start-reception'

    def __init__(self):
        service = os.environ.get(const.PEPPER_SERVICE, '')
        service_path = os.environ.get(const.PEPPER_SERVICEPATH, '')
        t = os.environ.get(const.PEPPER_TYPE, '')

        self.orion = Orion(service, service_path, t)
        self.pepper_1_id = os.environ.get(const.PEPPER_1_ID, '')

    def post(self):
        data = request.data.decode('utf-8')
        logger.info(f'request data={data}')

        result = {'result': 'failure'}
        try:
            value = self.orion.get_attr_value(data, 'state')
            if value is not None and value == 'on':
                message = self.orion.send_message(self.pepper_1_id, 'welcome', 'start')
                result['result'] = 'success'
                result['message'] = message
        except OrionError as e:
            logger.error(f'OrionError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)


class FinishReceptionAPI(MethodView):
    NAME = 'finish-reception'

    def __init__(self):
        service = os.environ.get(const.PEPPER_SERVICE, '')
        service_path = os.environ.get(const.PEPPER_SERVICEPATH, '')
        t = os.environ.get(const.PEPPER_TYPE, '')

        self.orion = Orion(service, service_path, t)
        self.pepper_1_id = os.environ.get(const.PEPPER_1_ID, '')

    def post(self):
        data = request.data.decode('utf-8')
        logger.info(f'request data={data}')

        result = {'result': 'failure'}
        try:
            value = self.orion.get_attr_value(data, 'dest')
            if value is not None:
                dest = Destination().get_destinations(value)

                if const.SLACK_WEBHOOK in dest:
                    slack.send_message_to_slack(dest[const.SLACK_WEBHOOK], dest.get(const.DEST_NAME))

                message = self.orion.send_message(self.pepper_1_id, 'handover', dest.get(const.DEST_FLOOR))
                result['result'] = 'success'
                result['message'] = message

        except DestinationDoesNotExist as e:
            logger.error(f'DestinationDoesNotFound: {str(e)}')
            raise BadRequest(str(e))
        except OrionError as e:
            logger.error(f'OrionError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)
