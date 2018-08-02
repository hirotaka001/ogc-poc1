# -*- coding: utf-8 -*-
import copy
import os
import re
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import NotFound

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
        'dest_pos': {
            'type': 'string',
            'pattern': '^(-)?[0-9]+(.[0-9]+)?,(-)?[0-9]+(.[0-9]+)?$',
        },
        'dest_led_id': {
            'type': 'string',
        },
        'dest_led_pos': {
            'type': 'string',
            'pattern': '^(-)?[0-9]+(.[0-9]+)?,(-)?[0-9]+(.[0-9]+)?$',
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
INSERT_SCHEMA['required'] = ['name', 'floor', 'dest_pos', 'dest_led_id', 'dest_led_pos', 'dest_human_sensor_id']


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

    def get(self):
        if 'pos.x' in request.args and 'pos.y' in request.args and 'floor' in request.args and request.args['floor'].isdigit():
            # TODO: fix logic
            dest_led_pos = f'{request.args["pos.x"]},{request.args["pos.y"]}'
            floor = int(request.args['floor'])
            filter_dict = {'dest_led_pos': dest_led_pos, 'floor': floor, 'initial': {'$ne': True}}
            return jsonify([utils.bson2dict(r) for r in self._collection.find(filter_dict)])

        if 'dest_human_sensor_id' in request.args:
            filter_dict = {'dest_human_sensor_id': request.args['dest_human_sensor_id'], 'initial': {'$ne': True}}
            return jsonify([utils.bson2dict(r) for r in self._collection.find(filter_dict)])

        if 'floor_initial' in request.args and request.args['floor_initial'].isdigit():
            filter_dict = {'initial': True, 'floor': int(request.args['floor_initial'])}
            return jsonify([utils.bson2dict(r) for r in self._collection.find(filter_dict)])

        if 'filter' in request.args:
            filter_dict = {'initial': {'$ne': True}}
            for f in [f.strip() for f in request.args['filter'].split(',')]:
                m = FILTER_RE.match(f)
                if m:
                    k = m.group('k')
                    v = m.group('v')
                    filter_dict[k] = int(v) if k == 'floor' and v.isdigit() else v
            result = [utils.bson2dict(r) for r in self._collection.find(filter_dict)]
        else:
            filter_dict = {'initial': {'$ne': True}}
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
