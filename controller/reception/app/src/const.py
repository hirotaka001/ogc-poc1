# -*- coding: utf-8 -*-

# logging
LOGGING_JSON = 'logging.json'
TARGET_HANDLERS = ['console', ]

# flask config
CONFIG_CFG = 'config.cfg'
DEFAULT_ORION_ENDPOINT = 'DEFAULT_ORION_ENDPOINT'
DEFAULT_PORT = 'DEFAULT_PORT'

# environment variable name
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
ORION_ENDPOINT = 'ORION_ENDPOINT'
PEPPER_SERVICE = 'PEPPER_SERVICE'
PEPPER_SERVICE_PATH = 'PEPPER_SERVICE_PATH'
PEPPER_TYPE = 'PEPPER_TYPE'
PEPPER_1_ID = 'PEPPER_1_ID'

# orion specification
ORION_PATH = '/v1/updateContext'
ORION_PAYLOAD_TEMPLATE = {
    'contextElements': [
        {
            'id': '',
            'isPattern': False,
            'type': '',
            'attributes': [
                {
                    'name': '',
                    'value': '',
                },
            ],
        },
    ],
    'updateAction': 'UPDATE',
}
