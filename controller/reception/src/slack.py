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
    try:
        r.raise_for_status()
        return r
    except requests.exceptions.HTTPError as e:
        logger.error(f'Slack API return Error : {str(r.status_code)}')
        logger.error(type(e))
        raise e
    else:
        logger.info(r)
