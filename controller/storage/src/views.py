# -*- coding: utf-8 -*-
import os
from logging import getLogger

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from PIL import Image

from src import const
from src.utils import get_random_str


logger = getLogger(__name__)

if const.FACE_UPLOAD_DIR_FULLPATH not in os.environ or \
        not os.environ[const.FACE_UPLOAD_DIR_FULLPATH].startswith('/') or \
        not os.path.isdir(os.environ[const.FACE_UPLOAD_DIR_FULLPATH]):
    msg = 'valid FACE_UPLOAD_DIR_FULLPATH does not set as an Environment Valiable'
    logger.fatal(msg)
    raise Exception(msg)

FACE_UPLOAD_DIR = os.environ[const.FACE_UPLOAD_DIR_FULLPATH]


class FaceListAPI(MethodView):
    NAME = 'face-list'

    def post(self):
        if 'face' not in request.files or not request.files['face']:
            msg = 'face image not found'
            logger.warning(msg)
            raise BadRequest(msg)
        imagefile = request.files['face']
        try:
            fmt = Image.open(imagefile.stream).format

            while True:
                filename = f'{get_random_str(16)}.{fmt}'
                path = os.path.join(FACE_UPLOAD_DIR, filename)
                if not os.path.isfile(path):
                    break

            imagefile.seek(0)
            imagefile.save(path)
            result = {
                'path': path,
                'url': '',
            }
            return jsonify(result)
        except OSError as e:
            msg = f'invalid face image, filename={imagefile.filename}, cause={str(e)}'
            logger.warning(msg)
            raise BadRequest(msg)
