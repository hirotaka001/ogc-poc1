# -*- coding: utf-8 -*-
import os
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const

from controllerlibs import DEST_NAME
from controllerlibs.services.orion import Orion, get_attr_value, NGSIPayloadError, AttrDoesNotExist

logger = getLogger(__name__)


class StartMovementAPI(MethodView):
    NAME = 'start-movement'

    def __init__(self):
        service = os.environ.get(const.ROBOT_SERVICE, '')
        service_path = os.environ.get(const.ROBOT_SERVICEPATH, '')
        self.type = os.environ.get(const.ROBOT_TYPE, '')
        self.id = os.environ.get(const.ROBOT_ID, '')
        self.turtlebot_1_id = os.environ.get(const.TURTLEBOT_1_ID, '')

        self.orion = Orion(service, service_path)

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            destx = get_attr_value(content, 'destx')
            desty = get_attr_value(content, 'desty')
            floor = get_attr_value(content, 'floor')
            if destx is not None and desty is not None and floor is not None:
                value = 'robot_id|{robot_id}|r_cmd|Navi|pos.x|{destx}|pos.y|{desty}|pos.z|{floor}'.format(
                    robot_id=self.turtlebot_1_id,
                    destx=destx,
                    desty=desty,
                    floor=floor,
                )
                message = self.orion.send_cmd(self.id, self.type, 'robot_request', value)
                result['result'] = 'success'
                result['message'] = message
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
