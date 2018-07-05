#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask

from controllerlibs import CONFIG_CFG, DEFAULT_PORT
from controllerlibs.utils import setup_logging, error_handler, get_port

from src.views import StartMovementAPI, CheckDestinationAPI, StopMovementAPI, ArrivalAPI

setup_logging()

app = Flask(__name__)
app.config.from_pyfile(CONFIG_CFG)
app.register_blueprint(error_handler.blueprint)
app.add_url_rule('/notify/start-movement/', view_func=StartMovementAPI.as_view(StartMovementAPI.NAME))
app.add_url_rule('/notify/check-destination/', view_func=CheckDestinationAPI.as_view(CheckDestinationAPI.NAME))
app.add_url_rule('/notify/stop-movement/', view_func=StopMovementAPI.as_view(StopMovementAPI.NAME))
app.add_url_rule('/notify/arrival/', view_func=ArrivalAPI.as_view(ArrivalAPI.NAME))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=get_port(app.config[DEFAULT_PORT]))
