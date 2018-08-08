# -*- coding: utf-8 -*-
import os
import json
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const

from controllerlibs.services.orion import Orion, get_id, get_attr_value, NGSIPayloadError, AttrDoesNotExist
from controllerlibs.services.destination import Destination, DestinationFormatError

logger = getLogger(__name__)


class RobotFloorMapMixin:
    def __init__(self):
        super().__init__()
        self.robot_floor_map = json.loads(os.environ.get(const.ROBOT_FLOOR_MAP, '{}'))

    def get_floor_by_robot(self, robot_id):
        return self.robot_floor_map[robot_id]

    def get_available_robot_from_floor(self, floor):
        return [r_id for r_id, f in self.robot_floor_map.items() if f == floor][0]


class StartMovementAPI(RobotFloorMapMixin, MethodView):
    NAME = 'start-movement'

    def __init__(self):
        super().__init__()
        service = os.environ.get(const.ROBOT_SERVICE, '')
        service_path = os.environ.get(const.ROBOT_SERVICEPATH, '')
        self.type = os.environ.get(const.ROBOT_TYPE, '')

        self.orion = Orion(service, service_path)

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            destx = get_attr_value(content, 'destx')
            desty = get_attr_value(content, 'desty')
            visitor_id = get_attr_value(content, 'visitor_id')

            try:
                floor = int(get_attr_value(content, 'floor'))
            except (TypeError, ValueError):
                raise DestinationFormatError('dest_floor is invalid')

            if destx is not None and desty is not None and floor in (1, 2) and visitor_id is not None:
                robot_id = self.get_available_robot_from_floor(floor)
                current_state = self.orion.get_attrs(robot_id, 'r_state')['r_state']['value'].strip()

                if current_state != const.WAITING:
                    message = f'cannot accept command at StartMovementAPI, current_state={current_state}, robot_id={robot_id} '\
                        f'destx={destx}, desty={desty}, floor={floor}, visitor_id={visitor_id}'
                    logger.warning(message)
                    result['result'] = 'not acceptable'
                    result['message'] = message
                else:
                    attributes = [
                        {
                            'name': 'r_state',
                            'value': const.GUIDING,
                        }, {
                            'name': 'destx',
                            'value': destx,
                        }, {
                            'name': 'desty',
                            'value': desty,
                        }, {
                            'name': 'visitor',
                            'value': visitor_id,
                        }
                    ]
                    self.orion.update_attributes(robot_id, self.type, attributes)

                    value = f'r_cmd|Navi|x|{destx}|y|{desty}'
                    message = self.orion.send_cmd(robot_id, self.type, 'robot_request', value)
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


class CheckDestinationAPI(RobotFloorMapMixin, MethodView):
    NAME = 'check-destination'

    def __init__(self):
        super().__init__()
        dest_led_service = os.environ.get(const.DEST_LED_SERVICE, '')
        dest_led_service_path = os.environ.get(const.DEST_LED_SERVICEPATH, '')
        self.dest_led_orion = Orion(dest_led_service, dest_led_service_path)

        robot_service = os.environ.get(const.ROBOT_SERVICE, '')
        robot_service_path = os.environ.get(const.ROBOT_SERVICEPATH, '')
        self.robot_orion = Orion(robot_service, robot_service_path)

        self.dest_led_type = os.environ.get(const.DEST_LED_TYPE, '')
        self.robot_type = os.environ.get(const.ROBOT_TYPE, '')

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'ignore'}
        try:
            r_mode = get_attr_value(content, 'r_mode')
            posx = get_attr_value(content, 'x')
            posy = get_attr_value(content, 'y')
            deviceid = get_id(content)
            floor = self.get_floor_by_robot(deviceid)
            logger.info(f'received position: r_mode={r_mode}, posx={posx}, posy={posy}, robot_id={deviceid}, floor={floor}')

            current_state = self.robot_orion.get_attrs(deviceid, 'r_state')['r_state']['value'].strip()

            if posx is not None and posy is not None and floor is not None and current_state == const.GUIDING:
                destination = Destination().get_destination_by_pos(posx, posy, floor)
                if destination is not None and const.DEST_LED_ID in destination and destination[const.DEST_LED_ID] is not None:
                    dest_led_id = destination[const.DEST_LED_ID]
                    message = self.dest_led_orion.send_cmd(dest_led_id, self.dest_led_type, 'action', 'on')
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


class StopMovementAPI(RobotFloorMapMixin, MethodView):
    NAME = 'stop-movement'

    def __init__(self):
        super().__init__()
        service = os.environ.get(const.ROBOT_SERVICE, '')
        service_path = os.environ.get(const.ROBOT_SERVICEPATH, '')
        self.type = os.environ.get(const.ROBOT_TYPE, '')

        self.orion = Orion(service, service_path)

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            r_mode = get_attr_value(content, 'r_mode')
            posx = get_attr_value(content, 'x')
            posy = get_attr_value(content, 'y')
            deviceid = get_id(content)
            floor = self.get_floor_by_robot(deviceid)
            logger.info(f'received position: r_mode={r_mode}, posx={posx}, posy={posy}, robot_id={deviceid}, floor={floor}')

            if r_mode == 'Standby':
                current_state = self.orion.get_attrs(deviceid, 'r_state')['r_state']['value'].strip()
                if current_state not in (const.GUIDING, const.RETURNING):
                    message = f'cannot accept command at StopMovmentAPI, current_state={current_state}, deviceid={deviceid} '\
                        f'r_mode={r_mode}, posx={posx}, posy={posy}, floor={floor}'
                    logger.warning(message)
                    result['result'] = 'not acceptable'
                    result['message'] = message
                else:
                    if current_state == const.GUIDING:
                        r_state = const.SUSPENDING
                    else:
                        r_state = const.WAITING

                    attributes = [
                        {
                            'name': 'r_state',
                            'value': r_state,
                        }
                    ]
                    message = self.orion.update_attributes(deviceid, self.type, attributes)
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


class ArrivalAPI(RobotFloorMapMixin, MethodView):
    NAME = 'arrival'

    def __init__(self):
        super().__init__()
        dest_led_service = os.environ.get(const.DEST_LED_SERVICE, '')
        dest_led_service_path = os.environ.get(const.DEST_LED_SERVICEPATH, '')
        self.dest_led_orion = Orion(dest_led_service, dest_led_service_path)

        robot_service = os.environ.get(const.ROBOT_SERVICE, '')
        robot_service_path = os.environ.get(const.ROBOT_SERVICEPATH, '')
        self.robot_orion = Orion(robot_service, robot_service_path)

        self.dest_led_type = os.environ.get(const.DEST_LED_TYPE, '')
        self.robot_type = os.environ.get(const.ROBOT_TYPE, '')

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
                if destination is not None and const.DEST_FLOOR in destination:
                    try:
                        floor = int(destination[const.DEST_FLOOR])
                    except (TypeError, ValueError):
                        raise DestinationFormatError('dest_floor is invalid')

                    robot_id = self.get_available_robot_from_floor(floor)
                    robot_attrs = self.robot_orion.get_attrs(robot_id, 'r_state,destx,desty')
                    current_state = robot_attrs['r_state']['value']
                    try:
                        destx = float(robot_attrs['destx']['value'])
                        desty = float(robot_attrs['desty']['value'])
                    except (TypeError, ValueError):
                        raise DestinationFormatError('destx or desty from guide_robot entity is not a float value')

                    if (current_state != const.SUSPENDING
                            or destx != float(destination.get(const.DEST_POS_X))
                            or desty != float(destination.get(const.DEST_POS_Y))):
                        message = f'cannot accept command at Arrival, current_state={current_state}, robot_id={robot_id}'\
                            f'destx={destx}, desty={desty}, floor={floor}'
                        logger.warning(message)
                        result['result'] = 'not acceptable'
                        result['message'] = message
                    else:
                        if const.DEST_LED_ID in destination and destination[const.DEST_LED_ID] is not None:
                            dest_led_id = destination[const.DEST_LED_ID]
                            self.dest_led_orion.send_cmd(dest_led_id, self.dest_led_type, 'action', 'off')

                        initial = destService.get_initial_of_floor(floor)
                        initial_pos_x = initial.get(const.DEST_POS_X)
                        initial_pos_y = initial.get(const.DEST_POS_Y)
                        if initial_pos_x is None or initial_pos_y is None:
                            raise DestinationFormatError('initial dest_pos_x or dest_pos_y is empty')

                        attributes = [
                            {
                                'name': 'r_state',
                                'value': const.RETURNING,
                            }, {
                                'name': 'destx',
                                'value': '',
                            }, {
                                'name': 'desty',
                                'value': '',
                            }
                        ]
                        self.robot_orion.update_attributes(robot_id, self.robot_type, attributes)

                        value = f'r_cmd|Navi|x|{initial_pos_x}|y|{initial_pos_y}'
                        message = self.robot_orion.send_cmd(robot_id, self.robot_type, 'robot_request', value)
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
