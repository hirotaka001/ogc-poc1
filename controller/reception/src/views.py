# -*- coding: utf-8 -*-
import os
import datetime
from logging import getLogger

import pytz

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import slack, const

from controllerlibs import DEST_NAME
from controllerlibs.services.orion import Orion, get_attr_value, NGSIPayloadError, AttrDoesNotExist
from controllerlibs.services.destination import Destination, DestinationDoesNotExist, DestinationFormatError

logger = getLogger(__name__)


class StartReceptionAPI(MethodView):
    NAME = 'start-reception'

    def __init__(self):
        service = os.environ.get(const.PEPPER_SERVICE, '')
        service_path = os.environ.get(const.PEPPER_SERVICEPATH, '')
        self.type = os.environ.get(const.PEPPER_TYPE, '')

        self.orion = Orion(service, service_path)
        self.pepper_1_id = os.environ.get(const.PEPPER_1_ID, '')

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            value = get_attr_value(content, 'state')
            if value == 'on':
                message = self.orion.send_cmd(self.pepper_1_id, self.type, 'welcome', 'start')
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
        self.type = os.environ.get(const.PEPPER_TYPE, '')

        self.orion = Orion(service, service_path)
        self.pepper_1_id = os.environ.get(const.PEPPER_1_ID, '')
        self.pepper_2_id = os.environ.get(const.PEPPER_2_ID, '')

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            value = get_attr_value(content, 'dest')
            dest = Destination().get_destination_by_name(value)
            dest_name = dest.get(DEST_NAME)
            if not dest_name:
                raise DestinationFormatError('dest_name is empty')
            try:
                dest_floor = int(dest.get(const.DEST_FLOOR))
            except (TypeError, ValueError):
                raise DestinationFormatError('dest_floor is invalid')

            if const.SLACK_WEBHOOK in dest:
                slack.send_message_to_slack(dest[const.SLACK_WEBHOOK], dest_name)

            if dest_floor == 1:
                logger.info(f'call start-movement to guide_robot, dest_name={dest_name}, floor={dest_floor}')
                self.__notify_start_movement(dest)
            elif dest_floor == 2:
                logger.info(f'call facedetect to pepper({self.pepper_2_id}), dest_name={dest_name}, floor={dest_floor}')
                self.orion.send_cmd(self.pepper_2_id, self.type, 'facedetect', 'start')
            else:
                logger.info(f'nothing to do, dest_name={dest_name}, floor={dest_floor}')

            message = self.orion.send_cmd(self.pepper_1_id, self.type, 'handover', dest_floor)
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
        except DestinationFormatError as e:
            logger.error(f'DestinationFormatError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)

    def __notify_start_movement(self, dest):
        dest_pos = dest.get(const.DEST_POS)
        if not dest_pos:
            raise DestinationFormatError('dest_pos is empty')
        try:
            destx, desty = [float(x.strip()) for x in dest_pos.split(',')]
            floor = int(dest.get(const.DEST_FLOOR))
        except (TypeError, ValueError):
            raise DestinationFormatError('invalid dest_pos or floor')
        else:
            timestamp = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            attributes = [
                {
                    'name': 'timestamp',
                    'value': timestamp,
                }, {
                    'name': 'destx',
                    'value': destx,
                }, {
                    'name': 'desty',
                    'value': desty,
                }, {
                    'name': 'floor',
                    'value': floor,
                }
            ]
            id = os.environ.get(const.START_MOVEMENT_ID, '')
            type = os.environ.get(const.START_MOVEMENT_TYPE, '')
            self.orion.update_attributes(id, type, attributes)
