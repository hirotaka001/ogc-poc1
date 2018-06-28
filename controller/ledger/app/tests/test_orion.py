# -*- coding: utf-8 -*-
import os

import pytest

import requests

from src.orion import send_request_to_orion
from src import const


class TestSendRequestToOrion:

    @pytest.mark.parametrize('v', [None, '', ' ', 'test value', '   test value 2   '])
    def test_success_no_env(self, monkeypatch, endpoint, mocked_post, v):
        mocked_post(monkeypatch, endpoint, '', '', '', '', v)
        send_request_to_orion(endpoint, v)

    @pytest.mark.parametrize('fs', ['', ' ', 'test service'])
    @pytest.mark.parametrize('fsp', ['', ' ', 'test servicepath'])
    @pytest.mark.parametrize('ri', ['', ' ', 'test robot id'])
    @pytest.mark.parametrize('rt', ['', ' ', 'test robot type'])
    @pytest.mark.parametrize('v', [None, '', ' ', 'test value', '   test value 2   '])
    def test_success_env(self, monkeypatch, endpoint, mocked_post, fs, fsp, ri, rt, v):
        os.environ[const.FIWARE_SERVICE] = fs
        os.environ[const.FIWARE_SERVICEPATH] = fsp
        os.environ[const.ROBOT_ID] = ri
        os.environ[const.ROBOT_TYPE] = rt

        mocked_post(monkeypatch, endpoint, fs, fsp, ri, rt, v)
        send_request_to_orion(endpoint, v)

    def test_raise_error(self, monkeypatch, endpoint):
        def mocked_post(endpoint, headers, data):
            raise requests.exceptions.RequestException()

        monkeypatch.setattr(requests, 'post', mocked_post)
        with pytest.raises(requests.exceptions.RequestException):
            send_request_to_orion(endpoint, 'dummy')
