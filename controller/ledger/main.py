#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

from controllerlibs import CONFIG_CFG, DEFAULT_PORT
from controllerlibs.utils import setup_logging, error_handler, get_port

from src.views import RecordReceptionAPI, RecordArrivalAPI

setup_logging()

app = Flask(__name__)
app.config.from_pyfile(CONFIG_CFG)
app.register_blueprint(error_handler.blueprint)
app.add_url_rule('/notify/record-reception/', view_func=RecordReceptionAPI.as_view(RecordReceptionAPI.NAME))
app.add_url_rule('/notify/record-arrival/', view_func=RecordArrivalAPI.as_view(RecordArrivalAPI.NAME))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=get_port(app.config[DEFAULT_PORT]))
