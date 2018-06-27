# -*- coding: utf-8 -*-
import os
import copy
import json
from urllib.parse import urljoin
from logging import getLogger

from flask import current_app

import requests

from src import const

logger = getLogger(__name__)


class OrionError(Exception):
    pass


class NGSIPayloadError(OrionError):
    pass


class Orion:
    ORION_GET_URL = None
    ORION_POST_URL = None

    @classmethod
    def get_orion_get_url(cls):
        if cls.ORION_GET_URL is None:
            if const.ORION_ENDPOINT in os.environ:
                cls.ORION_GET_URL = urljoin(os.environ[const.ORION_ENDPOINT], const.ORION_GET_PATH)
            else:
                cls.ORION_GET_URL = urljoin(current_app.config[const.DEFAULT_ORION_ENDPOINT], const.ORION_GET_PATH)
        return cls.ORION_GET_URL

    @classmethod
    def get_orion_post_url(cls):
        if cls.ORION_POST_URL is None:
            if const.ORION_ENDPOINT in os.environ:
                cls.ORION_POST_URL = urljoin(os.environ[const.ORION_ENDPOINT], const.ORION_POST_PATH)
            else:
                cls.ORION_POST_URL = urljoin(current_app.config[const.DEFAULT_ORION_ENDPOINT], const.ORION_POST_PATH)
        return cls.ORION_POST_URL

    def __init__(self, service, service_path, t):
        self.service = str(service)
        self.service_path = str(service_path)
        self.type = str(t)

    def get_attr_value(self, data, attr):
        if data is None or len(data.strip()) == 0:
            raise NGSIPayloadError()

        try:
            payload = json.loads(data)
        except json.decoder.JSONDecodeError:
            raise NGSIPayloadError()

        if (payload is None or not isinstance(payload, dict) or
                'data' not in payload or not isinstance(payload['data'], list)):
            raise NGSIPayloadError()

        for data in payload['data']:
            if (isinstance(data, dict) and attr in data and
                    isinstance(data[attr], dict) and 'value' in data[attr]):
                return data[attr]['value']

        return None

    def get_entity_ids(self, idpattern):
        headers = dict()
        headers['Fiware-Service'] = self.service
        headers['Fiware-Servicepath'] = self.service_path

        params = {
            'idPattern': os.environ.get(const.PEPPER_IDPATTERN, ''),
            'attrs': 'id',
        }

        response = requests.get(Orion.get_orion_get_url(), headers=headers, params=params)
        try:
            return [d['id'] for d in response.json()]
        except json.JSONDecodeError:
            raise NGSIPayloadError()

    def send_message(self, id, cmd, value):
        headers = dict()
        headers['Fiware-Service'] = self.service
        headers['Fiware-Servicepath'] = self.service_path
        headers['Content-Type'] = 'application/json'

        data = copy.deepcopy(const.ORION_PAYLOAD_TEMPLATE)
        data['contextElements'][0]['id'] = str(id)
        data['contextElements'][0]['isPattern'] = False
        data['contextElements'][0]['type'] = self.type
        data['contextElements'][0]['attributes'][0]['name'] = str(cmd)
        data['contextElements'][0]['attributes'][0]['value'] = str(value)

        requests.post(Orion.get_orion_post_url(), headers=headers, data=json.dumps(data))
        logger.debug(f'sent data to orion, headers={headers}, data={data}')
        return data
