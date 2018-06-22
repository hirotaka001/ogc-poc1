# -*- coding: utf-8 -*-
import os
import json
from logging import getLogger

from flask import request, jsonify, current_app
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const
from src.utils import get_random_str

logger = getLogger(__name__)

DESTINATIONS = [
  {
    "id": "dest-n4uRxmtdWv6jOHpI",
    "name": "管理センター",
    "floor": 1,
    "dest_pos": "0.001151,0.000134",
    "dest_led_id": "DEST-LED-CK2s264PqyndhUZ7",
    "dest_led_pos": "0.000000,0.000000",
    "dest_human_sensor_id": "DEST-HUMAN-SENSOR-n8aL7MJuNQk0iJpY"
  },
  {
    "id": "dest-vLBTZbPXc3Al0hMT",
    "name": "203号室",
    "floor": 2,
    "dest_pos": "125.12345,92.12345",
    "dest_led_id": "DEST-LED-12Mz9QcPjoemgU39",
    "dest_led_pos": "122.001122,91.991122",
    "dest_human_sensor_id": "DEST-HUMAN-SENSOR-oyVYENgHKHmQ6VJE"
  },
  {
    "id": "dest-9QgohxohSmb3AECD",
    "name": "204号室",
    "floor": 2,
    "dest_pos": "110.120101,0.993313",
    "dest_led_id": "DEST-LED-MV4isvEfDsLZ75R6",
    "dest_led_pos": "98.980808,0.881122",
    "dest_human_sensor_id": "DEST-HUMAN-SENSOR-9WfJoTmxczWrM4WZ"
  },
  {
    "id": "dest-Ymq1aoftEIViZjry",
    "name": "ProjectRoom 1",
    "floor": 3,
    "dest_pos": "125.12345,92.12345",
    "dest_led_id": "DEST-LED-sDAyKhjhXKqJsbr9",
    "dest_led_pos": "122.001122,91.991122",
    "dest_human_sensor_id": "DEST-HUMAN-SENSOR-6d8JoY1hR0wS8rqO",
    "slack_webhook": "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  }
]


class DestinationListAPI(MethodView):
    NAME = 'destination-list'

    def get(self):
        return jsonify(DESTINATIONS)
