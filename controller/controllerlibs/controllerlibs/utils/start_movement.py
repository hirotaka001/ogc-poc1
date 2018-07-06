# -*- coding: utf-8 -*-
import datetime

import pytz

from controllerlibs import DEST_POS, DEST_FLOOR
from controllerlibs.services.orion import Orion
from controllerlibs.services.destination import DestinationFormatError


def notify_start_movement(service, service_path, id, type, dest):
    dest_pos = dest.get(DEST_POS)
    if not dest_pos:
        raise DestinationFormatError('dest_pos is empty')
    try:
        destx, desty = [float(x.strip()) for x in dest_pos.split(',')]
        floor = int(dest.get(DEST_FLOOR))
    except (TypeError, ValueError):
        raise DestinationFormatError('invalid dest_pos or floor')
    else:
        timestamp = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        attributes = [
            {
                'name': 'timestamp',
                'value': timestamp,
            }, {
                'name': 'destx',
                'value': destx,
            }, {
                'name': 'desty',
                'value': desty,
            }, {
                'name': 'floor',
                'value': floor,
            }
        ]
        Orion(service, service_path).update_attributes(id, type, attributes)
