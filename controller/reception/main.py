#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

from controllerlibs import CONFIG_CFG, DEFAULT_PORT
from controllerlibs.utils import setup_logging, error_handler, get_port

from src.views import StartReceptionAPI, FinishReceptionAPI

setup_logging()

app = Flask(__name__)
app.config.from_pyfile(CONFIG_CFG)
app.register_blueprint(error_handler.blueprint)
app.add_url_rule('/notify/start-reception/', view_func=StartReceptionAPI.as_view(StartReceptionAPI.NAME))
app.add_url_rule('/notify/finish-reception/', view_func=FinishReceptionAPI.as_view(FinishReceptionAPI.NAME))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=get_port(app.config[DEFAULT_PORT]))
