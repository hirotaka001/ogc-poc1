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

from src import const, utils

from controllerlibs import DEST_NAME, DEST_FLOOR
from controllerlibs.services.orion import Orion, get_id, get_attr_value, NGSIPayloadError, AttrDoesNotExist
from controllerlibs.services.destination import Destination, DestinationDoesNotExist, DestinationFormatError
from controllerlibs.utils.start_movement import notify_start_movement

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

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        try:
            face = get_attr_value(content, 'face')
            dest = get_attr_value(content, 'dest')
            timestamp = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            data = {
                'status': 'reception',
                'face': face,
                'dest': Destination().get_destination_by_name(dest),
                'timestamps': [
                    {
                        'status': 'reception',
                        'timestamp': timestamp,
                    },
                ]
            }
            logger.info(f'record reception, data={data}')
            oid = self._collection.insert_one(data).inserted_id
            result = self._collection.find_one({"_id": oid})

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

        except AttrDoesNotExist as e:
            logger.error(f'AttrDoesNotExist: {str(e)}')
            raise BadRequest(str(e))
        except NGSIPayloadError as e:
            logger.error(f'NGSIPayloadError: {str(e)}')
            raise BadRequest(str(e))
        except Exception as e:
            logger.exception(e)
            raise e

        return jsonify(utils.bson2dict(result))


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
                        timestamps = utils.bson2dict(self._collection.find_one({"_id": ObjectId(visitor_id)}))['timestamps']
                        if not timestamps:
                            timestamps = list()
                        timestamps.append({
                            'status': 'arrival',
                            'timestamp': datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                        })
                        update_data = {
                            'status': 'arrival',
                            'timestamps': timestamps,
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
            # TODO: use FaceDetectAPI
            data = utils.bson2dict(self._collection.find({"status": "reception"}).sort([("timestamps", -1), ])[0])

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


class ReaskDestinationAPI(MethodView):
    NAME = 'reask-destination'

    def post(self):
        content = request.data.decode('utf-8')
        logger.info(f'request content={content}')

        result = {'result': 'failure'}

        return jsonify(result)
