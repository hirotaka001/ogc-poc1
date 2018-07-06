# -*- coding: utf-8 -*-
import os
import json
import datetime
from logging import getLogger

import pytz

import etcd3

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const

from controllerlibs import DEST_NAME, DEST_FLOOR
from controllerlibs.services.orion import Orion, get_id, get_attr_value, NGSIPayloadError, AttrDoesNotExist
from controllerlibs.services.destination import Destination, DestinationDoesNotExist, DestinationFormatError
from controllerlibs.utils.start_movement import notify_start_movement

logger = getLogger(__name__)


class RecordReceptionAPI(MethodView):
    NAME = 'record-reception'

    def __init__(self):
        self.etcd = etcd3.client(host=os.environ.get(const.ETCD_HOST))

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            face = get_attr_value(content, 'face')
            dest = get_attr_value(content, 'dest')
            timestamp = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            data = {
                'dest': Destination().get_destination_by_name(dest),
                'reception_timestamp': timestamp,
            }
            logger.info(f'record reception, face={face}, dest={dest}, timestamp={timestamp}')

            self.etcd.put(const.ETCD_DESTINATION_KEY, json.dumps(data))
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


class RecordArrivalAPI(MethodView):
    NAME = 'record-arrival'

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            id = get_id(content)
            arrival = get_attr_value(content, 'arrival')
            logger.info(f'record arrival, id={id}, arrival={arrival}')
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


class DetectVisitorAPI(MethodView):
    NAME = 'detect-visitor'

    def __init__(self):
        service = os.environ.get(const.PEPPER_SERVICE, '')
        service_path = os.environ.get(const.PEPPER_SERVICEPATH, '')
        self.type = os.environ.get(const.PEPPER_TYPE, '')

        self.orion = Orion(service, service_path)
        self.pepper_2_id = os.environ.get(const.PEPPER_2_ID, '')

        self.etcd = etcd3.client(host=os.environ.get(const.ETCD_HOST))

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            data = json.loads(self.etcd.get(const.ETCD_DESTINATION_KEY)[0].decode('utf-8'))

            dest_name = data['dest'].get(DEST_NAME)
            if not dest_name:
                raise DestinationFormatError('dest_name is empty')
            try:
                dest_floor = int(data['dest'].get(DEST_FLOOR))
            except (TypeError, ValueError):
                raise DestinationFormatError('dest_floor is invalid')

            if dest_floor == 2:
                logger.info(f'call start-movement to guide_robot, dest_name={dest_name}, floor={dest_floor}')
                notify_start_movement(os.environ.get(const.START_MOVEMENT_SERVICE, ''),
                                      os.environ.get(const.START_MOVEMENT_SERVICEPATH, ''),
                                      os.environ.get(const.START_MOVEMENT_ID, ''),
                                      os.environ.get(const.START_MOVEMENT_TYPE, ''),
                                      data['dest'])
            else:
                logger.warning(f'invalid floor, dest_name={dest_name}, floor={dest_floor}')

            message = self.orion.send_cmd(self.pepper_2_id, self.type, 'handover', 'continue')
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


class ReaskDestinationAPI(MethodView):
    NAME = 'reask-destination'

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}

        return jsonify(result)
