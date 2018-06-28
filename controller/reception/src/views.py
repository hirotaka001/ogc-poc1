# -*- coding: utf-8 -*-
import os
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import slack, const
from src.orion import Orion, get_attr_value, NGSIPayloadError, AttrDoesNotExist
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
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            value = get_attr_value(content, 'state')
            if value == 'on':
                message = self.orion.send_message(self.pepper_1_id, 'welcome', 'start')
                result['result'] = 'success'
                result['message'] = message
        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
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
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            value = get_attr_value(content, 'dest')
            dest = Destination().get_destinations(value)

            if const.SLACK_WEBHOOK in dest:
                slack.send_message_to_slack(dest[const.SLACK_WEBHOOK], dest.get(const.DEST_NAME))

            message = self.orion.send_message(self.pepper_1_id, 'handover', dest.get(const.DEST_FLOOR))
            result['result'] = 'success'
            result['message'] = message
        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
            raise BadRequest(str(e))
        except DestinationDoesNotExist as e:
            logger.error(f'DestinationDoesNotFound: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)
