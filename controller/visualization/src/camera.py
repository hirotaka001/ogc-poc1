# -*- coding: utf-8 -*-
import json
import os
import re
from logging import getLogger

from pytz import timezone
from dateutil import parser

from pymongo import MongoClient

from flask import request, render_template, jsonify, current_app, url_for
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const

logger = getLogger(__name__)


class CameraHeatmapPage(MethodView):
    NAME = 'camera-heatmap-page'

    def get(self):
        logger.info('CameraHeatmapPage#get')
        template = current_app.config[const.CAMERA_HEATMAP_TEMPLATE]

        bearer = os.environ.get(const.BEARER_AUTH, '')
        prefix = os.environ.get(const.PREFIX, '')

        if const.PREFIX in os.environ:
            positions_path = os.path.join('/',
                                          os.environ.get(const.PREFIX, '').strip(),
                                          *url_for(CameraHeatmapAPI.NAME).split(os.sep)[1:])
        else:
            positions_path = url_for(CameraHeatmapAPI.NAME)

        return render_template(template, bearer=bearer, path=positions_path, prefix=prefix)


class CameraHeatmapAPI(MethodView):
    NAME = 'camera-heatmap-api'

    ENDPOINT = os.environ[const.MONGODB_ENDPOINT]
    REPLICASET = os.environ[const.MONGODB_REPLICASET]
    DB = os.environ[const.MONGODB_DATABASE]
    COLLECTION_MAP = os.environ[const.MONGODB_COLLECTION_MAP]
    PIXEL_MAP = os.environ[const.PIXEL_MAP]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        client = MongoClient(CameraHeatmapAPI.ENDPOINT, replicaset=CameraHeatmapAPI.REPLICASET)
        self.db = client[CameraHeatmapAPI.DB]
        self.collection_map = json.loads(CameraHeatmapAPI.COLLECTION_MAP)
        self.pixel_map = json.loads(CameraHeatmapAPI.PIXEL_MAP)

    def get(self):
        logger.info(f'CameraHeatmapAPI#get')
        st = request.args.get('st')
        et = request.args.get('et')
        camera = request.args.get('camera')

        tz = current_app.config['TIMEZONE']

        logger.info(f'RobotPositionAPI, st={st} et={et} camera={camera}')
        if not st or not et:
            raise BadRequest({'message': 'empty query parameter "st" and/or "et"'})

        try:
            start_dt = parser.parse(st).astimezone(timezone(tz))
            end_dt = parser.parse(et).astimezone(timezone(tz))
        except (TypeError, ValueError):
            raise BadRequest({'message': 'invalid query parameter "st" and/or "et"'})

        logger.info(f'start_dt={start_dt}, end_dt={end_dt}')

        if camera not in self.collection_map:
            raise BadRequest({'message': 'unknown query parameter "camera"'})

        if camera not in self.pixel_map:
            raise BadRequest({'message': 'unknown query parameter "camera"'})

        if 'row' not in self.pixel_map[camera] \
                or 'column' not in self.pixel_map[camera] \
                or 'size' not in self.pixel_map[camera]:
            raise BadRequest({'message': 'invalid pixel_map'})

        row = self.pixel_map[camera]['row']
        column = self.pixel_map[camera]['column']
        pixel = self.pixel_map[camera]['size']

        collection = self.db[self.collection_map[camera]]

        dataset = [0] * row * column
        for data in collection.find({'c_mode': const.TARGET_C_MODE, 'recvTime': {'$gte': start_dt, '$lt': end_dt}}):
            if const.POSITION in data and const.NUM_P in data and data[const.NUM_P].isdecimal():
                for i in range(int(data[const.NUM_P])):
                    r = r'x\[{}\],(\d+).5/y\[{}\],(\d+)\.5'.format(i, i)
                    m = re.search(r, data['position'])
                    if m:
                        col_data = int(m.group(1))
                        row_data = int(m.group(2))
                        if col_data < column and row_data < row:
                            dataset[row_data * column + col_data] += 1

        result = {
            'row': row,
            'column': column,
            'pixel': pixel,
            'dataset': dataset,
        }

        return jsonify(result)
