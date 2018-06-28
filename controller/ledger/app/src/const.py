# -*- coding: utf-8 -*-

# logging
LOGGING_JSON = 'logging.json'
TARGET_HANDLERS = ['console', ]

# flask config
CONFIG_CFG = 'config.cfg'
DEFAULT_ORION_ENDPOINT = 'DEFAULT_ORION_ENDPOINT'
DEFAULT_PORT = 'DEFAULT_PORT'
DEFAULT_DESTINATION_ENDPOINT = 'DEFAULT_DESTINATION_ENDPOINT'

# environment variable name
LOG_LEVEL = 'LOG_LEVEL'
LISTEN_PORT = 'LISTEN_PORT'
ORION_ENDPOINT = 'ORION_ENDPOINT'
PEPPER_SERVICE = 'PEPPER_SERVICE'
PEPPER_SERVICEPATH = 'PEPPER_SERVICEPATH'
PEPPER_TYPE = 'PEPPER_TYPE'
PEPPER_IDPATTERN = 'PEPPER_IDPATTERN'
PEPPER_1_ID = 'PEPPER_1_ID'
DESTINATION_ENDPOINT = 'DESTINATION_ENDPOINT'

# orion specification
ORION_GET_PATH = '/v2/entities/'
ORION_POST_PATH = '/v1/updateContext'
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

# destination specification
DESTINATION_LIST_PATH = '/'
DEST_NAME = 'name'
DEST_FLOOR = 'floor'
SLACK_WEBHOOK = 'slack_webhook'
