# -*- coding: utf-8 -*-
import re
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import NotFound

logger = getLogger(__name__)

FILTER_RE = re.compile(r'^(?P<k>[^|]+)\|(?P<v>[^|]+)$')

DESTINATIONS = {
    "dest-n4uRxmtdWv6jOHpI": {
        "id": "dest-n4uRxmtdWv6jOHpI",
        "name": "管理センター",
        "floor": 1,
        "dest_pos": "0.001151,0.000134",
        "dest_led_id": "dest_led_0000000000000001",
        "dest_led_pos": "0.000000,0.000000",
        "dest_human_sensor_id": "dest_human_sensor_0000000000000001",
    },
    "dest-vLBTZbPXc3Al0hMT": {
        "id": "dest-vLBTZbPXc3Al0hMT",
        "name": "203号室",
        "floor": 2,
        "dest_pos": "125.12345,92.12345",
        "dest_led_id": "dest_led_0000000000000001",
        "dest_led_pos": "122.001122,91.991122",
        "dest_human_sensor_id": "dest_human_sensor_0000000000000001",
    },
    "dest-9QgohxohSmb3AECD": {
        "id": "dest-9QgohxohSmb3AECD",
        "name": "204号室",
        "floor": 2,
        "dest_pos": "110.120101,0.993313",
        "dest_led_id": "dest_led_0000000000000001",
        "dest_led_pos": "98.980808,0.881122",
        "dest_human_sensor_id": "dest_human_sensor_0000000000000001",
    },
    "dest-Ymq1aoftEIViZjry": {
        "id": "dest-Ymq1aoftEIViZjry",
        "name": "ProjectRoom 1",
        "floor": 3,
        "dest_pos": "125.12345,92.12345",
        "dest_led_id": "dest_led_0000000000000001",
        "dest_led_pos": "122.001122,91.991122",
        "dest_human_sensor_id": "dest_human_sensor_0000000000000001",
        "slack_webhook": "https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    },
}


class DestinationListAPI(MethodView):
    NAME = 'destination-list'

    def get(self):
        result = list(DESTINATIONS.values())

        if 'pos.x' in request.args and 'pos.y' in request.args and 'pos.z' in request.args:
            return jsonify(result[:1])

        if 'dest_human_sensor_id' in request.args:
            return jsonify(result[:1])

        if 'floor_initial' in request.args:
            if request.args['floor_initial'] == '1':
                return jsonify([{
                    "id": "dest-FtYNG505n7aIOJ0m",
                    "name": "1階初期位置",
                    "floor": 1,
                    "dest_pos": "0.0,0.0",
                    "dest_led_id": "dest_led_0000000000000001",
                    "dest_led_pos": "0.0,0.0",
                    "dest_human_sensor_id": "dest_human_sensor_0000000000000001",
                }])
            elif request.args['floor_initial'] == '2':
                return jsonify([{
                    "id": "dest-FtYNG505n7aIOJ0m",
                    "name": "1階初期位置",
                    "floor": 1,
                    "dest_pos": "0.0,0.0",
                    "dest_led_id": "dest_led_0000000000000001",
                    "dest_led_pos": "0.0,0.0",
                    "dest_human_sensor_id": "dest_human_sensor_0000000000000001",
                }])
            else:
                return jsonify([])

        if 'filter' in request.args:
            for f in [f.strip() for f in request.args['filter'].split(',')]:
                m = FILTER_RE.match(f)
                if f:
                    k = m.group('k')
                    v = m.group('v')
                    result = [r for r in result if k in r and str(r[k]) == str(v)]

        if 'attr' in request.args:
            attrs = [a.strip() for a in request.args['attr'].split(',')]
            result = [{k: d[k] for k in attrs if k in d} for d in result]

        return jsonify(result)


class DestinationDetailAPI(MethodView):
    NAME = 'destination-detail'

    def get(self, id):
        if id not in DESTINATIONS:
            raise NotFound()

        return jsonify(DESTINATIONS[id])
