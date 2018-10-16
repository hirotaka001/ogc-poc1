# -*- coding: utf-8 -*-
from logging import getLogger
import requests
import json

logger = getLogger(__name__)

def send_message_to_slack(webhook, room):
    message = f'来客がいらっしゃいました。{room}までご案内いたしております'
    logger.info(message)
    payload_dic = {
        "text":    message
    }
    r = requests.post(webhook, data=json.dumps(payload_dic))
    logger.info(r)
    if r.status_code != 200:
        logger.error(f'Slack API return Error : {str(r.status_code)}')
    return r
