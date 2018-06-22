# -*- coding: utf-8 -*-
import copy
import json
from logging import getLogger

import requests

from src import const

logger = getLogger(__name__)


class OrionError(Exception):
    pass


class NGSIPayloadError(OrionError):
    pass


def get_attr_value(data, attr):
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


def send_message(endpoint, service, service_path, id, type, cmd, value, isPattern=False):
    headers = dict()
    headers['Fiware-Service'] = str(service)
    headers['Fiware-Servicepath'] = str(service_path)
    headers['Content-Type'] = 'application/json'

    data = copy.deepcopy(const.ORION_PAYLOAD_TEMPLATE)
    data['contextElements'][0]['id'] = str(id)
    data['contextElements'][0]['isPattern'] = isPattern
    data['contextElements'][0]['type'] = str(type)
    data['contextElements'][0]['attributes'][0]['name'] = str(cmd)
    data['contextElements'][0]['attributes'][0]['value'] = str(value)

    requests.post(endpoint, headers=headers, data=json.dumps(data))
    logger.debug(f'sent data to orion, headers={headers}, data={data}')
    return data
