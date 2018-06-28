# -*- coding: utf-8 -*-
import os
import copy
import json
from urllib.parse import urljoin
from logging import getLogger

from flask import current_app

import requests

from controllerlibs import ORION_ENDPOINT, ORION_GET_PATH, ORION_POST_PATH, ORION_PAYLOAD_TEMPLATE, DEFAULT_ORION_ENDPOINT

logger = getLogger(__name__)


class OrionError(Exception):
    pass


class NGSIPayloadError(OrionError):
    pass


class AttrDoesNotExist(OrionError):
    pass


class Orion:
    ORION_GET_URL = None
    ORION_POST_URL = None

    @classmethod
    def get_orion_get_url(cls):
        if cls.ORION_GET_URL is None:
            if ORION_ENDPOINT in os.environ:
                cls.ORION_GET_URL = urljoin(os.environ[ORION_ENDPOINT], ORION_GET_PATH)
            else:
                cls.ORION_GET_URL = urljoin(current_app.config[DEFAULT_ORION_ENDPOINT], ORION_GET_PATH)
        return cls.ORION_GET_URL

    @classmethod
    def get_orion_post_url(cls):
        if cls.ORION_POST_URL is None:
            if ORION_ENDPOINT in os.environ:
                cls.ORION_POST_URL = urljoin(os.environ[ORION_ENDPOINT], ORION_POST_PATH)
            else:
                cls.ORION_POST_URL = urljoin(current_app.config[DEFAULT_ORION_ENDPOINT], ORION_POST_PATH)
        return cls.ORION_POST_URL

    def __init__(self, service, service_path, t):
        self.service = str(service)
        self.service_path = str(service_path)
        self.type = str(t)

    def get_entity_ids(self, idpattern):
        headers = dict()
        headers['Fiware-Service'] = self.service
        headers['Fiware-Servicepath'] = self.service_path

        params = {
            'idPattern': idpattern,
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

        data = copy.deepcopy(ORION_PAYLOAD_TEMPLATE)
        data['contextElements'][0]['id'] = str(id)
        data['contextElements'][0]['isPattern'] = False
        data['contextElements'][0]['type'] = self.type
        data['contextElements'][0]['attributes'][0]['name'] = str(cmd)
        data['contextElements'][0]['attributes'][0]['value'] = str(value)

        requests.post(Orion.get_orion_post_url(), headers=headers, data=json.dumps(data))
        logger.debug(f'sent data to orion, headers={headers}, data={data}')
        return data


def get_attr_value(content, attr):
    data = __extract_attr_from_NGSI(content, attr)
    return data['value']


def get_attr_timestamp(content, attr):
    data = __extract_attr_from_NGSI(content, attr)
    return data['metadata']['TimeInstant']['value']


def __extract_attr_from_NGSI(content, attr):
    if content is None or len(content.strip()) == 0:
        raise NGSIPayloadError()

    try:
        payload = json.loads(content)
    except json.decoder.JSONDecodeError:
        raise NGSIPayloadError()

    if (payload is None or not isinstance(payload, dict) or
            'data' not in payload or not isinstance(payload['data'], list)):
        raise NGSIPayloadError()

    for data in payload['data']:
        if (isinstance(data, dict) and attr in data and
                isinstance(data[attr], dict) and 'value' in data[attr]):
            return data[attr]

    raise AttrDoesNotExist(attr)
