# -*- coding: utf-8 -*-
import datetime

import pytz

from controllerlibs import DEST_POS_X, DEST_POS_Y, DEST_FLOOR
from controllerlibs.services.orion import Orion
from controllerlibs.services.destination import DestinationFormatError


def notify_start_movement(service, service_path, id, type, dest, visitor_id):
    dest_pos_x = dest.get(DEST_POS_X)
    dest_pos_y = dest.get(DEST_POS_Y)
    if dest_pos_x is None or dest_pos_y is None:
        raise DestinationFormatError('dest_pos_x or dest_pos_y is empty')
    try:
        destx = float(dest_pos_x)
        desty = float(dest_pos_y)
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
            }, {
                'name': 'visitor_id',
                'value': visitor_id,
            }
        ]
        Orion(service, service_path).update_attributes(id, type, attributes)
