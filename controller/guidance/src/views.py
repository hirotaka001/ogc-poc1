# -*- coding: utf-8 -*-
import os
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const

from controllerlibs.services.orion import Orion, get_attr_value, NGSIPayloadError, AttrDoesNotExist
from controllerlibs.services.destination import Destination, DestinationFormatError

logger = getLogger(__name__)


class StartMovementAPI(MethodView):
    NAME = 'start-movement'

    def __init__(self):
        service = os.environ.get(const.ROBOT_SERVICE, '')
        service_path = os.environ.get(const.ROBOT_SERVICEPATH, '')
        self.type = os.environ.get(const.ROBOT_TYPE, '')
        self.id = os.environ.get(const.ROBOT_ID, '')
        self.turtlebot_1_id = os.environ.get(const.TURTLEBOT_1_ID, '')

        self.orion = Orion(service, service_path)

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            destx = get_attr_value(content, 'destx')
            desty = get_attr_value(content, 'desty')
            floor = get_attr_value(content, 'floor')
            if destx is not None and desty is not None and floor is not None:
                value = 'robot_id|{robot_id}|r_cmd|Navi|pos.x|{destx}|pos.y|{desty}|pos.z|{floor}'.format(
                    robot_id=self.turtlebot_1_id,
                    destx=destx,
                    desty=desty,
                    floor=floor,
                )
                message = self.orion.send_cmd(self.id, self.type, 'robot_request', value)
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


class CheckDestinationAPI(MethodView):
    NAME = 'check-destination'

    def __init__(self):
        service = os.environ.get(const.DEST_LED_SERVICE, '')
        service_path = os.environ.get(const.DEST_LED_SERVICEPATH, '')
        self.type = os.environ.get(const.DEST_LED_TYPE, '')

        self.orion = Orion(service, service_path)

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'ignore'}
        try:
            posx = get_attr_value(content, 'pos.x')
            posy = get_attr_value(content, 'pos.y')
            posz = get_attr_value(content, 'pos.z')

            if posx is not None and posy is not None and posz is not None:
                destination = Destination().get_dest_led_by_pos(posx, posy, posz)
                if destination is not None and const.DEST_LED_ID in destination:
                    dest_led_id = destination[const.DEST_LED_ID]
                    message = self.orion.send_cmd(dest_led_id, self.type, 'action', 'on')
                    result['result'] = 'success'
                    result['message'] = message
        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
            raise BadRequest(str(e))
        except DestinationFormatError as e:
            logger.error(f'DestinationFormatError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)
