# -*- coding: utf-8 -*-
from logging import getLogger
import requests
import json

logger = getLogger(__name__)


def send_message_to_slack(webhook, room):
    dest = {'dest 1-1': 'ホワイトボード室',
            'dest 1-2': '会議室１',
            'dest 1-3': '会議室２',
            'dest 1-4': '会議室３',
            'dest 2-1': '会津若松市　情報政策課',
            'dest 2-2': '株式会社シンク',
            'dest 2-3': '株式会社ソニックス',
            'ProjectRoom 1': 'TIS株式会社'}

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
