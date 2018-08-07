# -*- coding: utf-8 -*-
import json

from bson import json_util


def bson2dict(bson):
    raw = json.loads(json_util.dumps(bson, ensure_ascii=False))
    oid = raw['_id']['$oid']
    del raw['_id']
    raw['id'] = oid
    return raw
