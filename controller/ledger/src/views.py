# -*- coding: utf-8 -*-
import os
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const
from src.orion import get_attr_value, get_attr_timestamp, NGSIPayloadError, AttrDoesNotExist

logger = getLogger(__name__)


class RecordReceptionAPI(MethodView):
    NAME = 'record-reception'

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            face = get_attr_value(content, 'face')
            dest = get_attr_value(content, 'dest')
            timestamp = get_attr_timestamp(content, 'dest')
            logger.info(f'face={face}, dest={dest}, timestamp={timestamp}')
        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)
