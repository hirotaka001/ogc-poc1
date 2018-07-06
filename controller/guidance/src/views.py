# -*- coding: utf-8 -*-
import os
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const

from controllerlibs.services.orion import Orion, get_id, get_attr_value, NGSIPayloadError, AttrDoesNotExist
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
        self.turtlebot_2_id = os.environ.get(const.TURTLEBOT_2_ID, '')

        self.orion = Orion(service, service_path)

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            destx = get_attr_value(content, 'destx')
            desty = get_attr_value(content, 'desty')
            try:
                floor = int(get_attr_value(content, 'floor'))
            except (TypeError, ValueError):
                raise DestinationFormatError('dest_floor is invalid')

            if destx is not None and desty is not None and floor in (1, 2):
                turtlebot_id = self.turtlebot_1_id if floor == 1 else self.turtlebot_2_id
                value = f'robot_id|{turtlebot_id}|r_cmd|Navi|pos.x|{destx}|pos.y|{desty}|pos.z|{floor}'
                message = self.orion.send_cmd(self.id, self.type, 'robot_request', value)
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
                destination = Destination().get_destination_by_pos(posx, posy, posz)
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


class StopMovementAPI(MethodView):
    NAME = 'stop-movement'

    def __init__(self):
        pass

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        logger.info('nothing to do when called stop-movement')
        result = {'result': 'nothing to do'}

        return jsonify(result)


class ArrivalAPI(MethodView):
    NAME = 'arrival'

    def __init__(self):
        dest_led_service = os.environ.get(const.DEST_LED_SERVICE, '')
        dest_led_service_path = os.environ.get(const.DEST_LED_SERVICEPATH, '')
        self.dest_led_orion = Orion(dest_led_service, dest_led_service_path)

        robot_service = os.environ.get(const.ROBOT_SERVICE, '')
        robot_service_path = os.environ.get(const.ROBOT_SERVICEPATH, '')
        self.robot_orion = Orion(robot_service, robot_service_path)

        self.dest_led_type = os.environ.get(const.DEST_LED_TYPE, '')
        self.robot_type = os.environ.get(const.ROBOT_TYPE, '')
        self.robot_id = os.environ.get(const.ROBOT_ID, '')
        self.turtlebot_1_id = os.environ.get(const.TURTLEBOT_1_ID, '')
        self.turtlebot_2_id = os.environ.get(const.TURTLEBOT_2_ID, '')

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'ignore'}
        try:
            arrival = get_attr_value(content, 'arrival')
            if arrival is not None:
                id = get_id(content)
                destService = Destination()
                destination = destService.get_destination_by_dest_human_sensor_id(id)
                if destination is not None and const.DEST_LED_ID in destination:
                    dest_led_id = destination[const.DEST_LED_ID]
                    message = self.dest_led_orion.send_cmd(dest_led_id, self.dest_led_type, 'action', 'off')
                if destination is not None and const.DEST_FLOOR in destination:
                    try:
                        floor = int(destination[const.DEST_FLOOR])
                    except (TypeError, ValueError):
                        raise DestinationFormatError('dest_floor is invalid')

                    turtlebot_id = self.turtlebot_1_id if floor == 1 else self.turtlebot_2_id
                    initial = destService.get_initial_of_floor(floor)
                    initial_pos = initial.get(const.DEST_POS)
                    if not initial_pos:
                        raise DestinationFormatError('initial dest_pos is empty')
                    initx, inity = [float(x.strip()) for x in initial_pos.split(',')]
                    value = f'robot_id|{turtlebot_id}|r_cmd|Navi|pos.x|{initx}|pos.y|{inity}|pos.z|{floor}'
                    message = self.robot_orion.send_cmd(self.robot_id, self.robot_type, 'robot_request', value)
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
