# -*- coding: utf-8 -*-
import os

# logging
LOGGING_JSON = os.environ.get('LOGGING_JSON', '../docker/logging.json')
TARGET_HANDLERS = ['console', ]

# flask config
CONFIG_CFG = 'config.cfg'
DEFAULT_PORT = 'DEFAULT_PORT'
DEFAULT_UPLOAD_DIR = 'DEFAULT_UPLOAD_DIR'

# environment variable name
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
FACE_UPLOAD_DIR_FULLPATH = 'FACE_UPLOAD_DIR_FULLPATH'
