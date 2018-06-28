# -*- coding: utf-8 -*-
import os

# logging
LOGGING_JSON = os.environ.get('LOGGING_JSON', '../docker/logging.json')
TARGET_HANDLERS = ['console', ]

# flask config
CONFIG_CFG = 'config.cfg'
DEFAULT_PORT = 'DEFAULT_PORT'

# environment variable name
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
