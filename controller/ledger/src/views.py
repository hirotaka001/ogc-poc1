# -*- coding: utf-8 -*-
import os
import json
import datetime
from logging import getLogger

import pytz

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from pymongo import MongoClient
from bson.objectid import ObjectId

import cognitive_face as CF

from src import const, utils

from controllerlibs import DEST_NAME, DEST_FLOOR
from controllerlibs.services.orion import Orion, get_id, get_attr_value, NGSIPayloadError, AttrDoesNotExist
from controllerlibs.services.destination import Destination, DestinationDoesNotExist, DestinationFormatError
from controllerlibs.utils.start_movement import notify_start_movement

if const.FACE_API_KEY in os.environ:
    CF.Key.set(os.environ[const.FACE_API_KEY])
if const.FACE_API_BASEURL in os.environ:
    CF.BaseUrl.set(os.environ[const.FACE_API_BASEURL])

logger = getLogger(__name__)


class MongoMixin:
    def __init__(self):
        super().__init__()
        url = os.environ.get(const.MONGODB_URL, 'mongodb://localhost:27017')
        rs = os.environ.get(const.MONGODB_REPLICASET, None)

        if rs:
            client = MongoClient(url, replicaset=rs)
        else:
            client = MongoClient(url)
        self._collection = client[const.MONGODB_DATABASE][const.MONGODB_COLLECTION]


class RobotFloorMapMixin:
    def __init__(self):
        super().__init__()
        self.robot_floor_map = json.loads(os.environ.get(const.ROBOT_FLOOR_MAP, '{}'))

    def get_available_robot_from_floor(self, floor):
        return [r_id for r_id, f in self.robot_floor_map.items() if f == floor][0]


class RecordReceptionAPI(MongoMixin, MethodView):
    NAME = 'record-reception'

    def __init__(self):
        super().__init__()
        service = os.environ.get(const.PEPPER_SERVICE, '')
        service_path = os.environ.get(const.PEPPER_SERVICEPATH, '')
        self.type = os.environ.get(const.PEPPER_TYPE, '')

        self.orion = Orion(service, service_path)
        self.pepper_1_id = os.environ.get(const.PEPPER_1_ID, '')

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            face = get_attr_value(content, 'face')
            dest = get_attr_value(content, 'dest')
            timestamp = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

            if face and os.path.isfile(face):
                face_ids = [r['faceId'] for r in CF.face.detect(face)]
            else:
                face_ids = []
                face = None

            data = {
                'status': 'reception',
                'face': face,
                'faceIds': face_ids,
                'dest': Destination().get_destination_by_name(dest),
                'receptionDatetime': timestamp,
            }
            logger.info(f'record reception, data={data}')
            oid = self._collection.insert_one(data).inserted_id
            self._collection.find_one({"_id": oid})

            dest_name = data['dest'].get(DEST_NAME)
            try:
                dest_floor = int(data['dest'].get(DEST_FLOOR))
            except (TypeError, ValueError):
                raise DestinationFormatError('dest_floor is invalid')

            if dest_floor == 1:
                logger.info(f'call start-movement to guide_robot, dest_name={dest_name}, floor={dest_floor}')
                notify_start_movement(os.environ.get(const.START_MOVEMENT_SERVICE, ''),
                                      os.environ.get(const.START_MOVEMENT_SERVICEPATH, ''),
                                      os.environ.get(const.START_MOVEMENT_ID, ''),
                                      os.environ.get(const.START_MOVEMENT_TYPE, ''),
                                      data['dest'], str(oid))
            else:
                logger.info(f'nothing to do, dest_name={dest_name}, floor={dest_floor}')

            message = self.orion.send_cmd(self.pepper_1_id, self.type, 'handover', dest_floor)
            result['result'] = 'success'
            result['message'] = message
        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)


class RecordArrivalAPI(RobotFloorMapMixin, MongoMixin, MethodView):
    NAME = 'record-arrival'

    def __init__(self):
        super().__init__()
        service = os.environ.get(const.ROBOT_SERVICE, '')
        service_path = os.environ.get(const.ROBOT_SERVICEPATH, '')
        self.type = os.environ.get(const.ROBOT_TYPE, '')

        self.orion = Orion(service, service_path)

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            id = get_id(content)
            arrival = get_attr_value(content, 'arrival')
            if arrival is not None:
                destination = Destination().get_destination_by_dest_human_sensor_id(id)
                if destination is not None and const.DEST_FLOOR in destination:
                    try:
                        floor = int(destination[const.DEST_FLOOR])
                    except (TypeError, ValueError):
                        raise DestinationFormatError('dest_floor is invalid')

                    robot_id = self.get_available_robot_from_floor(floor)
                    visitor_id = self.orion.get_attrs(robot_id, 'visitor')['visitor']['value'].strip()

                    if visitor_id:
                        timestamp = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                        update_data = {
                            'status': 'arrival',
                            'arrivalDatetime': timestamp,
                        }
                        self._collection.update_one({"_id": ObjectId(visitor_id)}, {"$set": update_data})

                        attributes = [
                            {
                                'name': 'visitor',
                                'value': '',
                            }
                        ]
                        message = self.orion.update_attributes(robot_id, self.type, attributes)
                        result['result'] = 'success'
                        result['message'] = message
            logger.info(f'record arrival, id={id}, arrival={arrival}')
        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)


class DetectVisitorAPI(MongoMixin, MethodView):
    NAME = 'detect-visitor'

    def __init__(self):
        super().__init__()
        service = os.environ.get(const.PEPPER_SERVICE, '')
        service_path = os.environ.get(const.PEPPER_SERVICEPATH, '')
        self.type = os.environ.get(const.PEPPER_TYPE, '')

        self.orion = Orion(service, service_path)
        self.pepper_2_id = os.environ.get(const.PEPPER_2_ID, '')

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            face = get_attr_value(content, 'face')

            if face and os.path.isfile(face):
                face_ids = [result['faceId'] for result in CF.face.detect(face)]
            else:
                return jsonify(self.__send_reask())

            now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            visitors = [utils.bson2dict(d) for d in self._collection.find({
                'status': 'reception',
                'dest.floor': 2,
                'receptionDatetime': {'$gte': now - datetime.timedelta(minutes=const.FACE_VERIFY_DELTA_MIN)},
            }).sort([('receptionDatetime', -1), ])]

            def verify(visitors):
                for visitor in visitors:
                    for visitor_fid in visitor['faceIds']:
                        for fid in face_ids:
                            res = CF.face.verify(visitor_fid, fid)
                            res['visitor'] = visitor
                            yield res
                            if res['isIdentical']:
                                raise StopIteration
            verified = list(verify(visitors))
            if len(verified) == 0 or not verified[-1]['isIdentical']:
                return jsonify(self.__send_reask())
            else:
                logger.info(f'face api verify: identical result, {verified[-1]}')
                data = verified[-1]['visitor']

            dest_name = data['dest'].get(DEST_NAME)
            if not dest_name:
                raise DestinationFormatError('dest_name is empty')
            try:
                dest_floor = int(data['dest'].get(DEST_FLOOR))
            except (TypeError, ValueError):
                raise DestinationFormatError('dest_floor is invalid')

            if dest_floor == 2:
                logger.info(f'call start-movement to guide_robot, dest_name={dest_name}, floor={dest_floor}')
                notify_start_movement(os.environ.get(const.START_MOVEMENT_SERVICE, ''),
                                      os.environ.get(const.START_MOVEMENT_SERVICEPATH, ''),
                                      os.environ.get(const.START_MOVEMENT_ID, ''),
                                      os.environ.get(const.START_MOVEMENT_TYPE, ''),
                                      data['dest'], data['id'])
            else:
                logger.warning(f'invalid floor, dest_name={dest_name}, floor={dest_floor}')

            message = self.orion.send_cmd(self.pepper_2_id, self.type, 'handover', 'continue')
            result['result'] = 'success'
            result['message'] = message
        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
            raise BadRequest(str(e))
        except DestinationDoesNotExist as e:
            logger.error(f'DestinationDoesNotFound: {str(e)}')
            raise BadRequest(str(e))
        except DestinationFormatError as e:
            logger.error(f'DestinationFormatError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)

    def __send_reask(self):
        try:
            message = self.orion.send_cmd(self.pepper_2_id, self.type, 'reask', 'true')
            result = {
                'result': 'success',
                'message': message,
            }
        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return result


class ReaskDestinationAPI(MongoMixin, MethodView):
    NAME = 'reask-destination'

    def __init__(self):
        super().__init__()
        service = os.environ.get(const.PEPPER_SERVICE, '')
        service_path = os.environ.get(const.PEPPER_SERVICEPATH, '')
        self.type = os.environ.get(const.PEPPER_TYPE, '')

        self.orion = Orion(service, service_path)
        self.pepper_2_id = os.environ.get(const.PEPPER_2_ID, '')

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}
        try:
            dest = get_attr_value(content, 'dest')
            timestamp = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

            data = {
                'status': 'reask',
                'face': None,
                'faceIds': [],
                'dest': Destination().get_destination_by_name(dest),
                'reaskDatetime': timestamp,
            }
            logger.info(f'record reask, data={data}')
            oid = self._collection.insert_one(data).inserted_id

            dest_name = data['dest'].get(DEST_NAME)
            try:
                dest_floor = int(data['dest'].get(DEST_FLOOR))
            except (TypeError, ValueError):
                raise DestinationFormatError('dest_floor is invalid')

            if dest_floor == 2:
                logger.info(f'call start-movement to guide_robot, dest_name={dest_name}, floor={dest_floor}')
                notify_start_movement(os.environ.get(const.START_MOVEMENT_SERVICE, ''),
                                      os.environ.get(const.START_MOVEMENT_SERVICEPATH, ''),
                                      os.environ.get(const.START_MOVEMENT_ID, ''),
                                      os.environ.get(const.START_MOVEMENT_TYPE, ''),
                                      data['dest'], str(oid))
            else:
                logger.info(f'nothing to do, dest_name={dest_name}, floor={dest_floor}')

            message = self.orion.send_cmd(self.pepper_2_id, self.type, 'handover', 'continue')
            result['result'] = 'success'
            result['message'] = message
        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(result)
