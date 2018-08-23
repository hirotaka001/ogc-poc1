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
            'anyOf': [{
                'type': 'number',
            }, {
                'type': 'null',
            }],
        },
        'dest_pos_y': {
            'anyOf': [{
                'type': 'number',
            }, {
                'type': 'null',
            }],
        },
        'dest_led_id': {
            'anyOf': [{
                'type': 'string',
            }, {
                'type': 'null',
            }],
        },
        'dest_led_pos_x': {
            'anyOf': [{
                'type': 'number',
            }, {
                'type': 'null',
            }],
        },
        'dest_led_pos_y': {
            'anyOf': [{
                'type': 'number',
            }, {
                'type': 'null',
            }],
        },
        'dest_human_sensor_id': {
            'anyOf': [{
                'type': 'string',
            }, {
                'type': 'null',
            }],
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


class DuplicateKeyError(Exception):
    pass


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

    def check_duplication(self, data):
        try:
            if (data.get('name') is not None
                    and self._collection.find({"name": data['name']}).count() > 0):
                raise DuplicateKeyError(f'name({data["name"]}) is duplicate')
            if (data.get('dest_led_id') is not None
                    and self._collection.find({"dest_led_id": data['dest_led_id']}).count() > 0):
                raise DuplicateKeyError(f'dest_led_id({data["dest_led_id"]}) is duplicate')
            if (data.get('dest_human_sensor_id') is not None
                    and self._collection.find({"dest_human_sensor_id": data['dest_human_sensor_id']}).count() > 0):
                raise DuplicateKeyError(f'dest_human_sensor_id({data["dest_human_sensor_id"]}) is duplicate')
            if (data.get('dest_pos_x') is not None and data.get('dest_pos_y') is not None
                    and self._collection.find({"floor": data['floor'],
                                               "dest_pos_x": data['dest_pos_x'],
                                               "dest_pos_y": data['dest_pos_y']}).count() > 0):
                raise DuplicateKeyError(f'floor({data["floor"]}) and dest_pos_x({data["dest_pos_x"]}) '
                                        f'and dest_pos_y({data["dest_pos_y"]}) is duplicate')
            if (data.get('dest_led_pos_x') is not None and data.get('dest_led_pos_y') is not None
                    and self._collection.find({"floor": data['floor'],
                                               "dest_led_pos_x": data['dest_led_pos_x'],
                                               "dest_led_pos_y": data['dest_led_pos_y']}).count() > 0):
                raise DuplicateKeyError(f'floor({data["floor"]}) and dest_led_pos_x({data["dest_led_pos_x"]}) '
                                        f'and dest_led_pos_y({data["dest_led_pos_y"]}) is duplicate')
        except DuplicateKeyError as e:
            logger.warning(str(e))
            raise e


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

        filter_dict = dict()
        if 'include_initial' not in request.args or request.args['include_initial'] != 'true':
            filter_dict = {'initial': {'$ne': True}}
        if 'filter' in request.args:
            for f in [f.strip() for f in request.args['filter'].split(',')]:
                m = FILTER_RE.match(f)
                if m:
                    k = m.group('k')
                    v = m.group('v')
                    if k not in UPDATE_SCHEMA['properties'] or k == 'initial':
                        continue

                    if 'type' in UPDATE_SCHEMA['properties'][k]:
                        ktypes = (UPDATE_SCHEMA['properties'][k]['type'], )
                    elif 'anyOf' in UPDATE_SCHEMA['properties'][k]:
                        ktypes = tuple([a['type'] for a in UPDATE_SCHEMA['properties'][k]['anyOf']])
                    else:
                        continue

                    if 'integer' in ktypes:
                        try:
                            v = int(v)
                        except (TypeError, ValueError):
                            pass
                    elif 'number' in ktypes:
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
        try:
            self.check_duplication(data)
        except DuplicateKeyError as e:
            msg = f'insert error : {str(e)}'
            logger.warning(msg)
            raise BadRequest(msg)
        else:
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
        try:
            self.check_duplication(data)
        except DuplicateKeyError as e:
            msg = f'insert error : {str(e)}'
            logger.warning(msg)
            raise BadRequest(msg)
        else:
            self._collection.update_one({"_id": ObjectId(id)}, {"$set": data})
            return self.get(id)

    def delete(self, id):
        self._collection.delete_one({"_id": ObjectId(id)})
        return ('', 204)
