# -*- coding: utf-8 -*-
import json
from logging import getLogger

from flask import request
from werkzeug.exceptions import BadRequest

import jsonschema

from bson import json_util

logger = getLogger(__name__)


def validate_json(schema):
    if not request.headers.get('Content-Type') == 'application/json':
        msg = f'invalid Content-Type: {request.headers.get("Content-Type")}'
        logger.warning(msg)
        raise BadRequest(msg)
    try:
        data = request.json
        if not data:
            msg = f'request json is empty'
            logger.warning(msg)
            raise BadRequest(msg)
        jsonschema.validate(data, schema)
        return data
    except jsonschema.exceptions.ValidationError as e:
        msg = f'request json validation error: {e.message}'
        logger.warning(msg)
        raise BadRequest(msg)
    except Exception as e:
        msg = f'request json parse error: {str(e)}'
        logger.warning(msg)
        raise BadRequest(msg)


def bson2dict(bson):
    raw = json.loads(json_util.dumps(bson, ensure_ascii=False))
    oid = raw['_id']['$oid']
    del raw['_id']
    raw['id'] = oid
    return raw
