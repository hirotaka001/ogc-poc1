# -*- coding: utf-8 -*-
import os
from logging import getLogger
from urllib.parse import urljoin

from flask import request, jsonify, current_app
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import orion
from src import const

logger = getLogger(__name__)


class OrionEndpointMixin:
    ORION_ENDPOINT = None

    @classmethod
    def get_orion_endpoint(cls):
        if cls.ORION_ENDPOINT is None:
            if const.ORION_ENDPOINT in os.environ:
                cls.ORION_ENDPOINT = urljoin(os.environ[const.ORION_ENDPOINT], const.ORION_PATH)
            else:
                cls.ORION_ENDPOINT = urljoin(current_app.config[const.DEFAULT_ORION_ENDPOINT], const.ORION_PATH)
        return cls.ORION_ENDPOINT


class StartReceptionAPI(OrionEndpointMixin, MethodView):
    NAME = 'start-reception'

    def post(self):
        data = request.data.decode('utf-8')
        logger.info(f'request data={data}')

        result = {'result': 'failure'}
        try:
            value = orion.get_attr_value(data, 'state')
            if value is not None:
                endpoint = StartReceptionAPI.get_orion_endpoint()
                service = os.environ.get(const.PEPPER_SERVICE, '')
                service_path = os.environ.get(const.PEPPER_SERVICE_PATH, '')
                id = os.environ.get(const.PEPPER_1_ID, '')
                type = os.environ.get(const.PEPPER_TYPE, '')
                message = orion.send_message(endpoint, service, service_path, id, type, 'welcome', 'start')
                result['result'] = 'success'
                result['message'] = message
        except orion.OrionError as e:
            logger.error(f'OrionError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)
