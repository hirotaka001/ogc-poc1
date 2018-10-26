#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

from controllerlibs import CONFIG_CFG, DEFAULT_PORT
from controllerlibs.utils import setup_logging, error_handler, get_port

from src.camera import CameraHeatmapPage, CameraHeatmapAPI

setup_logging()

app = Flask(__name__)
app.config.from_pyfile(CONFIG_CFG)
app.register_blueprint(error_handler.blueprint)
app.add_url_rule('/camera/heatmap/', view_func=CameraHeatmapPage.as_view(CameraHeatmapPage.NAME))
app.add_url_rule('/camera/data/', view_func=CameraHeatmapAPI.as_view(CameraHeatmapAPI.NAME))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=get_port(app.config[DEFAULT_PORT]))
