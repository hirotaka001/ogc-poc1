# -*- cofing: utf-8 -*-
import os
import json
from urllib.parse import urljoin

import pytest

import requests

import main
from src import const


@pytest.fixture
def endpoint():
    return urljoin(main.app.config[const.DEFAULT_ORION_ENDPOINT], const.ORION_PATH)


@pytest.fixture
def mocked_post():
    def setup(monkeypatch, ep, fs, fsp, ri, rt, v):
        counter = type('', (), {'count': 0})()

        def mock_func(endpoint, headers, data):
            assert endpoint == ep
            assert isinstance(headers, dict)
            assert headers == {
                'Fiware-Service': fs,
                'Fiware-Servicepath': fsp,
                'Content-Type': 'application/json',
            }
            assert isinstance(data, str)
            assert json.loads(data) == {
                'contextElements': [
                    {
                        'id': ri,
                        'isPattern': False,
                        'type': rt,
                        'attributes': [
                            {
                                'name': 'move',
                                'type': 'string',
                                'value': v,
                            }
                        ],
                    }
                ],
                'updateAction': 'UPDATE',
            }
            counter.count += 1
        monkeypatch.setattr(requests, 'post', mock_func)
        return counter
    return setup


@pytest.fixture
def client():
    return main.app.test_client()


@pytest.fixture(scope='function', autouse=True)
def teardown():
    yield
    if const.FIWARE_SERVICE in os.environ:
        del os.environ[const.FIWARE_SERVICE]
    if const.FIWARE_SERVICEPATH in os.environ:
        del os.environ[const.FIWARE_SERVICEPATH]
    if const.ROBOT_ID in os.environ:
        del os.environ[const.ROBOT_ID]
    if const.ROBOT_TYPE in os.environ:
        del os.environ[const.ROBOT_TYPE]
    if const.PREFIX in os.environ:
        del os.environ[const.PREFIX]
