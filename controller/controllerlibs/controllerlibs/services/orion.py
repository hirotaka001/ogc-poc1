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

    def __init__(self, service, service_path):
        self.service = str(service)
        self.service_path = str(service_path)

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

    def send_cmd(self, id, type, cmd, value):
        attributes = [
            {
                'name': str(cmd),
                'value': str(value),
            }
        ]
        return self.__update_context(id, type, attributes)

    def update_attributes(self, id, type, attributes):
        if not isinstance(attributes, list):
            raise NGSIPayloadError()
        for attr in attributes:
            if not isinstance(attr, dict) or 'name' not in attr or 'value' not in attr:
                raise NGSIPayloadError()

        return self.__update_context(id, type, attributes)

    def __update_context(self, id, type, attributes):
        headers = dict()
        headers['Fiware-Service'] = self.service
        headers['Fiware-Servicepath'] = self.service_path
        headers['Content-Type'] = 'application/json'

        data = copy.deepcopy(ORION_PAYLOAD_TEMPLATE)
        data['contextElements'][0]['id'] = str(id)
        data['contextElements'][0]['isPattern'] = False
        data['contextElements'][0]['type'] = str(type)
        data['contextElements'][0]['attributes'] = attributes

        requests.post(Orion.get_orion_post_url(), headers=headers, data=json.dumps(data))
        logger.debug(f'sent data to orion, headers={headers}, data={data}')
        return data


def get_id(content):
    for data in __extract_data_from_NGSI(content):
        if isinstance(data, dict) and 'id' in data:
            return data['id']

    raise AttrDoesNotExist('id')


def get_attr_value(content, attr):
    data = __extract_attr_from_NGSI(content, attr)
    return data['value']


def get_attr_timestamp(content, attr):
    data = __extract_attr_from_NGSI(content, attr)
    return data['metadata']['TimeInstant']['value']


def __extract_attr_from_NGSI(content, attr):
    for data in __extract_data_from_NGSI(content):
        if (isinstance(data, dict) and attr in data and
                isinstance(data[attr], dict) and 'value' in data[attr]):
            return data[attr]

    raise AttrDoesNotExist(attr)


def __extract_data_from_NGSI(content):
    if content is None or len(content.strip()) == 0:
        raise NGSIPayloadError()

    try:
        payload = json.loads(content)
    except json.decoder.JSONDecodeError:
        raise NGSIPayloadError()

    if (payload is None or not isinstance(payload, dict) or
            'data' not in payload or not isinstance(payload['data'], list)):
        raise NGSIPayloadError()

    return payload['data']
