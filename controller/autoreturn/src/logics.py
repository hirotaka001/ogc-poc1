# -*- coding: utf-8 -*-
import os
import json
import datetime
from logging import getLogger

from pytz import timezone
from dateutil import parser

from src import const

from controllerlibs.services.orion import Orion
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


class AutoReturner(RobotFloorMapMixin):
    def __init__(self, suspending_sec_max):
        super().__init__()
        self.suspending_sec_max = suspending_sec_max

        robot_service = os.environ.get(const.ROBOT_SERVICE, '')
        robot_service_path = os.environ.get(const.ROBOT_SERVICEPATH, '')
        self.robot_orion = Orion(robot_service, robot_service_path)
        self.robot_type = os.environ.get(const.ROBOT_TYPE, '')

        self.destService = Destination()

    def check_robot(self, floor):
        try:
            robot_id = self.get_available_robot_from_floor(floor)
            robot_attrs = self.robot_orion.get_attrs(robot_id, 'r_state')
            current_state = robot_attrs['r_state']['value']
            current_datetime = parser.parse(robot_attrs['r_state']['metadata']['TimeInstant']['value'])
            now = datetime.datetime.now(timezone('Asia/Tokyo'))
            delta_sec = (now - current_datetime).total_seconds()

            if current_state != const.SUSPENDING or delta_sec < self.suspending_sec_max:
                logger.debug(f'nothing to do')
            else:
                initial = self.destService.get_initial_of_floor(floor)
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
                self.robot_orion.send_cmd(robot_id, self.robot_type, 'robot_request', value)
                logger.info(f'guide_robot({robot_id} return to the initial position of floor({floor}) automatically')
        except Exception as e:
            logger.exception(e)
            raise e
