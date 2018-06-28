# -*- coding: utf-8 -*-
import os
import json
import string
import random
import logging.config
from logging import getLogger

from controllerlibs import LOGGING_JSON, TARGET_HANDLERS, LOG_LEVEL, LISTEN_PORT


def setup_logging():
    try:
        with open(LOGGING_JSON, "r") as f:
            logging.config.dictConfig(json.load(f))
            if (LOG_LEVEL in os.environ and
                    os.environ[LOG_LEVEL].upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
                for handler in getLogger().handlers:
                    if handler.get_name() in TARGET_HANDLERS:
                        handler.setLevel(getattr(logging, os.environ[LOG_LEVEL].upper()))
    except FileNotFoundError:
        pass


def get_port(default_port):

    try:
        port = int(os.environ.get(LISTEN_PORT, str(default_port)))
        if port < 1 or 65535 < port:
            port = default_port
    except ValueError:
        port = default_port

    return port


def get_random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])
