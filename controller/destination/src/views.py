# -*- coding: utf-8 -*-
import copy
import os
import re
from logging import getLogger

from flask import request, jsonify, current_app
from flask.views import MethodView
from werkzeug.exceptions import NotFound, BadRequest

from pymongo import MongoClient

from bson.objectid import ObjectId
from bson.errors import InvalidId

from src import const, utils

logger = getLogger(__name__)

FILTER_RE = re.compile(r'^(?P<k>[^|]+)\|(?P<v>[^|]+)$')

UPDATE_SCHEMA = {
    'type': 'object',
    'properties': {
        'name': {
            'type': 'string',
        },
        'floor': {
            'type': 'integer',
            'minimum': 1,
        },
        'dest_pos_x': {
            'type': 'number',
        },
        'dest_pos_y': {
            'type': 'number',
        },
        'dest_led_id': {
            'type': 'string',
        },
        'dest_led_pos_x': {
            'type': 'number',
        },
        'dest_led_pos_y': {
            'type': 'number',
        },
        'dest_human_sensor_id': {
            'type': 'string',
        },
        'slack_webhook': {
            'type': 'string',
        },
        'initial': {
            'type': 'boolean',
        },
    },
    'additionalProperties': False,
}
INSERT_SCHEMA = copy.copy(UPDATE_SCHEMA)
INSERT_SCHEMA['required'] = ['name', 'floor', 'dest_pos_x', 'dest_pos_y', 'dest_led_id',
                             'dest_led_pos_x', 'dest_led_pos_y', 'dest_human_sensor_id']


class MongoMixin:
    def __init__(self):
        super().__init__()
        url = os.environ.get(const.MONGODB_URL, 'mongodb://localhost:27017')
        rs = os.environ.get(const.MONGODB_REPLICASET, None)

        if rs:
            client = MongoClient(url, replicaset=rs)
        else:
            client = MongoClient(url)
        self._collection = client[const.MONGODB_DATABASE][const.MONGODB_COLLECTION]


class DestinationListAPI(MongoMixin, MethodView):
    NAME = 'destination-list'

    def __init__(self):
        super().__init__()
        if const.POS_DELTA in os.environ:
            try:
                self.pos_delta = float(os.environ[const.POS_DELTA])
            except (TypeError, ValueError):
                self.pos_delta = current_app.config[const.DEFAULT_POS_DELTA]
        else:
            self.pos_delta = current_app.config[const.DEFAULT_POS_DELTA]

    def get(self):
        if 'pos.x' in request.args and 'pos.y' in request.args and 'floor' in request.args:
            try:
                pos_x = float(request.args['pos.x'])
                pos_y = float(request.args['pos.y'])
                floor = int(request.args['floor'])
            except (TypeError, ValueError) as e:
                msg = f'invalid query parameter(s) : {str(e)}'
                logger.warning(msg)
                raise BadRequest(msg)
            else:
                filter_dict = {
                    'dest_led_pos_x': {
                        '$gte': pos_x - self.pos_delta,
                        '$lte': pos_x + self.pos_delta,
                    },
                    'dest_led_pos_y': {
                        '$gte': pos_y - self.pos_delta,
                        '$lte': pos_y + self.pos_delta,
                    },
                    'floor': floor,
                    'initial': {
                        '$ne': True,
                    }
                }
                return jsonify([utils.bson2dict(r) for r in self._collection.find(filter_dict)])

        if 'dest_human_sensor_id' in request.args:
            filter_dict = {'dest_human_sensor_id': request.args['dest_human_sensor_id'], 'initial': {'$ne': True}}
            return jsonify([utils.bson2dict(r) for r in self._collection.find(filter_dict)])

        if 'floor_initial' in request.args:
            try:
                floor = int(request.args['floor_initial'])
            except (TypeError, ValueError) as e:
                msg = f'invalid query parameter(s) : {str(e)}'
                logger.warning(msg)
                raise BadRequest(msg)
            else:
                filter_dict = {'initial': True, 'floor': floor}
                return jsonify([utils.bson2dict(r) for r in self._collection.find(filter_dict)])

        filter_dict = {'initial': {'$ne': True}}
        if 'filter' in request.args:
            for f in [f.strip() for f in request.args['filter'].split(',')]:
                m = FILTER_RE.match(f)
                if m:
                    k = m.group('k')
                    v = m.group('v')
                    if k not in UPDATE_SCHEMA['properties'] or k == 'initial':
                        continue
                    if UPDATE_SCHEMA['properties'][k]['type'] == 'integer':
                        try:
                            v = int(v)
                        except (TypeError, ValueError):
                            pass
                    elif UPDATE_SCHEMA['properties'][k]['type'] == 'number':
                        try:
                            v = float(v)
                        except (TypeError, ValueError):
                            pass
                    filter_dict[k] = v

            result = [utils.bson2dict(r) for r in self._collection.find(filter_dict)]
        else:
            result = [utils.bson2dict(r) for r in self._collection.find(filter_dict)]

        if 'attr' in request.args:
            attrs = [a.strip() for a in request.args['attr'].split(',')]
            result = [{k: d[k] for k in attrs if k in d} for d in result]

        return jsonify(result)

    def post(self):
        data = utils.validate_json(INSERT_SCHEMA)
        oid = self._collection.insert_one(data).inserted_id
        result = self._collection.find_one({"_id": oid})
        return jsonify(utils.bson2dict(result))


class DestinationDetailAPI(MongoMixin, MethodView):
    NAME = 'destination-detail'

    def __init__(self):
        super().__init__()

    def get(self, id):
        try:
            bson = self._collection.find_one({"_id": ObjectId(id)})
            if bson:
                return jsonify(utils.bson2dict(bson))
            else:
                raise NotFound(f'{id} does not found')
        except InvalidId as e:
            raise NotFound(f'{id} is invalid: {str(e)}')

    def put(self, id):
        data = utils.validate_json(UPDATE_SCHEMA)
        self._collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return self.get(id)

    def delete(self, id):
        self._collection.delete_one({"_id": ObjectId(id)})
        return ('', 204)
