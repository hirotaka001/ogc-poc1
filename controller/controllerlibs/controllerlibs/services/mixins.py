# -*- coding: utf-8 -*-
import os
import json

from controllerlibs import ROBOT_FLOOR_MAP


class RobotFloorMapMixin:
    def __init__(self):
        super().__init__()
        self.robot_floor_map = json.loads(os.environ.get(ROBOT_FLOOR_MAP, '{}'))

    def get_floor_by_robot(self, robot_id):
        return self.robot_floor_map[robot_id]

    def get_available_robot_from_floor(self, floor):
        return [r_id for r_id, f in self.robot_floor_map.items() if f == floor][0]
