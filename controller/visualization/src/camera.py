# -*- coding: utf-8 -*-
import os
import datetime
from logging import getLogger

from pytz import timezone
from dateutil import parser

from flask import request, render_template, jsonify, current_app, url_for
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from src import const

logger = getLogger(__name__)


class CameraHeatmapPage(MethodView):
    NAME = 'camera-heatmap-page'

    def get(self):
        logger.info('CameraHeatmapPage#get')
        template = current_app.config[const.CAMERA_HEATMAP_TEMPLATE]

        bearer = os.environ.get(const.BEARER_AUTH, '')
        prefix = os.environ.get(const.PREFIX, '')

        if const.PREFIX in os.environ:
            positions_path = os.path.join('/',
                                          os.environ.get(const.PREFIX, '').strip(),
                                          *url_for(CameraHeatmapAPI.NAME).split(os.sep)[1:])
        else:
            positions_path = url_for(CameraHeatmapAPI.NAME)

        return render_template(template, bearer=bearer, path=positions_path, prefix=prefix)


class CameraHeatmapAPI(MethodView):
    NAME = 'camera-heatmap-api'

    def get(self):
        logger.info('CameraHeatmapAPI#get')
        return jsonify({})
