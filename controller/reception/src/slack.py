# -*- coding: utf-8 -*-
from logging import getLogger
import requests
import json

logger = getLogger(__name__)


def send_message_to_slack(webhook, room):
    dest = {'ProjectRoom 1': 'プロジェクトルーム1',
            'ProjectRoom 2': 'プロジェクトルーム2',
            'ProjectRoom 3': 'プロジェクトルーム3'}
    if room not in dest:
        logger.error(f'The destination does not exist : {room}')
        return room
    message = f'来客がいらっしゃいました。{dest[room]}までご案内いたしております'
    logger.info(message)
    payload_dic = {
        "text":    message
    }
    try:
        r = requests.post(webhook, data=json.dumps(payload_dic))
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        logger.error(e)
        raise e
    else:
        logger.debug(r)
