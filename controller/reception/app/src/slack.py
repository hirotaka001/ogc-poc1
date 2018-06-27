# -*- coding: utf-8 -*-
from logging import getLogger

logger = getLogger(__name__)


def send_message_to_slack(webhook, name):
    message = f'来客がいらっしゃいました。{name}までご案内いたしております'
    logger.info(message)
