#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import signal
import time
from logging import getLogger

from src import const
from src.logics import AutoReturner

from controllerlibs.utils import setup_logging

setup_logging()
logger = getLogger(__name__)

STOP_FLAG = False


def stop_handler(signal, frame):
    global STOP_FLAG
    STOP_FLAG = True


signal.signal(signal.SIGTERM, stop_handler)


def main():
    logger.info('start main loop')
    try:
        interval_sec = int(os.environ.get(const.INTERVAL_SEC, None))
    except (ValueError, TypeError):
        interval_sec = const.DEFAULT_INTERVAL_SEC

    try:
        suspending_sec_max = int(os.environ.get(const.SUSPENDING_SEC_MAX, None))
    except (ValueError, TypeError):
        suspending_sec_max = const.DEFAULT_SUSPENDING_SEC_MAX

    returner = AutoReturner(suspending_sec_max)
    while not STOP_FLAG:
        for floor in const.TARGET_FLOOR:
            returner.check_robot(floor)
        time.sleep(interval_sec)
    logger.info('stop main loop')


if __name__ == '__main__':
    main()
