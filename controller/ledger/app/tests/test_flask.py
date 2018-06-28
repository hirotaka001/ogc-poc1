# -*- coding: utf-8 -*-
import json
import os
from urllib.parse import urlparse

import pytest
from pyquery import PyQuery as pq

import requests

from src import const


class TestGamepadAPI:

    @pytest.mark.parametrize('v', [None, '', ' ', 'test value', '   test value 2   '])
    def test_success_no_env(self, monkeypatch, endpoint, mocked_post, client, v):
        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', v.strip() if v is not None else None)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = client.post('/gamepad/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        if v is not None and len(v.strip()) != 0:
            assert response.json == {'result': 'ok', 'requested': True, 'value': v.strip()}
            assert counter.count == 1
        else:
            assert response.json == {'result': 'ok', 'requested': False}
            assert counter.count == 0

    @pytest.mark.parametrize('fs', ['', ' ', 'test service'])
    @pytest.mark.parametrize('fsp', ['', ' ', 'test servicepath'])
    @pytest.mark.parametrize('ri', ['', ' ', 'test robot id'])
    @pytest.mark.parametrize('rt', ['', ' ', 'test robot type'])
    @pytest.mark.parametrize('v', [None, '', ' ', 'test value', '   test value 2   '])
    def test_success_env(self, monkeypatch, endpoint, mocked_post, client, fs, fsp, ri, rt, v):
        os.environ[const.FIWARE_SERVICE] = fs
        os.environ[const.FIWARE_SERVICEPATH] = fsp
        os.environ[const.ROBOT_ID] = ri
        os.environ[const.ROBOT_TYPE] = rt

        counter = mocked_post(monkeypatch, endpoint, fs, fsp, ri, rt, v.strip() if v is not None else None)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = client.post('/gamepad/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        if v is not None and len(v.strip()) != 0:
            assert response.json == {'result': 'ok', 'requested': True, 'value': v.strip()}
            assert counter.count == 1
        else:
            assert response.json == {'result': 'ok', 'requested': False}
            assert counter.count == 0

    def test_raise_error(self, monkeypatch, endpoint, client):
        v = 'dummy'

        def mocked_post(endpoint, headers, data):
            raise requests.exceptions.RequestException()

        monkeypatch.setattr(requests, 'post', mocked_post)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = client.post('/gamepad/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        assert response.json == {'error': 'Internal Server Error'}

    @pytest.mark.parametrize('data', ['EMPTY', None, '', ' ', 1, 'a=b', [],
                                      {}, {'data': ''}, {'data': 1}, {'data': {}}, {'data': None}])
    def test_bad_request1(self, monkeypatch, endpoint, mocked_post, client, data):
        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', 'dummy')

        if data == 'EMPTY':
            response = client.post('/gamepad/', content_type='application/json')
        else:
            response = client.post('/gamepad/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        assert response.json == {'error': 'Bad Request'}
        assert counter.count == 0

    @pytest.mark.parametrize('data', [{'data': []}, {'data': ['', ]}, {'data': [0, ]}, {'data': [None, ]},
                                      {'data': [{}, ]}, {'data': [{'invalid': 'dummy'}, ]},
                                      {'data': [{'button': ''}, ]}, {'data': [{'button': 1}, ]}, {'data': [{'button': None}, ]},
                                      {'data': [{'button': {}}, ]}, {'data': [{'button': {'invalid': 'dummy'}}, ]},
                                      {'data': [{'button': {'value': None}}, ]}, {'data': [{'button': {'value': 1}}, ]},
                                      {'data': [{'button': {'value': []}}, ]}, {'data': [{'button': {'value': {}}}, ]}])
    def test_bad_request2(self, monkeypatch, endpoint, mocked_post, client, data):
        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', 'dummy')
        response = client.post('/gamepad/', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        assert response.json == {'result': 'ok', 'requested': False}
        assert counter.count == 0

    def test_moved_permanentry(self, monkeypatch, endpoint, mocked_post, client):
        v = 'dummy'

        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', v.strip() if v is not None else None)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = client.post('/gamepad', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 301
        assert response.content_type == 'text/html; charset=utf-8'
        assert counter.count == 0

    @pytest.mark.parametrize('method', ['get', 'put', 'patch', 'delete', 'head'])
    @pytest.mark.parametrize('path', ['/gamepad/', '/gamepad'])
    def test_method_not_allowed(self, monkeypatch, endpoint, mocked_post, client, method, path):
        v = 'dummy'

        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', v.strip() if v is not None else None)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = getattr(client, method)(path, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 405
        assert response.content_type == 'application/json'
        if method != 'head':
            assert response.json == {'error': 'Method Not Allowed'}
        assert counter.count == 0


class TestWebAPI:

    def test_head(self, client):
        response = client.head('/web/')
        assert response.status_code == 200
        assert not hasattr(response, 'body')

    def test_get(self, client):
        response = client.get('/web/')
        assert response.status_code == 200
        assert response.content_type == 'text/html; charset=utf-8'
        q = pq(response.data.decode('utf-8'), parser='html')
        assert q.find('title').text() == 'Web Controller'
        assert len(q.find('h3.text-muted')) == 1
        assert q.find('h3.text-muted').text() == 'Web controller'
        assert len(q.find('form[method="POST"]')) == 1
        assert len(q.find('button[type="submit"][name="move"][value="up"]')) == 1
        assert q.find('button[type="submit"][name="move"][value="up"]').text() == '↑'
        assert len(q.find('button[type="submit"][name="move"][value="left"]')) == 1
        assert q.find('button[type="submit"][name="move"][value="left"]').text() == '←'
        assert len(q.find('button[type="submit"][name="move"][value="right"]')) == 1
        assert q.find('button[type="submit"][name="move"][value="right"]').text() == '→'
        assert len(q.find('button[type="submit"][name="move"][value="down"]')) == 1
        assert q.find('button[type="submit"][name="move"][value="down"]').text() == '↓'
        assert len(q.find('button[type="submit"][name="move"][value="triangle"]')) == 1
        assert q.find('button[type="submit"][name="move"][value="triangle"]').text() == '△'
        assert len(q.find('button[type="submit"][name="move"][value="square"]')) == 1
        assert q.find('button[type="submit"][name="move"][value="square"]').text() == '□'
        assert len(q.find('button[type="submit"][name="move"][value="circle"]')) == 1
        assert q.find('button[type="submit"][name="move"][value="circle"]').text() == '○'
        assert len(q.find('button[type="submit"][name="move"][value="cross"]')) == 1
        assert q.find('button[type="submit"][name="move"][value="cross"]').text() == '☓'

    @pytest.mark.parametrize('v', [None, '', ' ', 'test value', '   test value 2   '])
    def test_post_no_env(self, monkeypatch, endpoint, mocked_post, client, v):
        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', v.strip() if v is not None else None)

        response = client.post('/web/', data=dict(move=v), follow_redirects=False)
        assert response.status_code == 302
        assert response.content_type == 'text/html; charset=utf-8'
        assert urlparse(response.location).path == '/web/'
        if v is not None and len(v.strip()) != 0:
            assert counter.count == 1
        else:
            assert counter.count == 0

    @pytest.mark.parametrize('fs', ['', ' ', 'test service'])
    @pytest.mark.parametrize('fsp', ['', ' ', 'test servicepath'])
    @pytest.mark.parametrize('ri', ['', ' ', 'test robot id'])
    @pytest.mark.parametrize('rt', ['', ' ', 'test robot type'])
    @pytest.mark.parametrize('p', ['', ' ',
                                   'prefix', '/prefix', 'prefix/', '/prefix/', '  prefix  ',
                                   'prefix/1', '/prefix/1', 'prefix/1/', '/prefix/1/', '  prefix/1  '])
    @pytest.mark.parametrize('v', [None, '', ' ', 'test value', '   test value 2   '])
    def test_success_env(self, monkeypatch, endpoint, mocked_post, client, fs, fsp, ri, rt, p, v):
        os.environ[const.FIWARE_SERVICE] = fs
        os.environ[const.FIWARE_SERVICEPATH] = fsp
        os.environ[const.ROBOT_ID] = ri
        os.environ[const.ROBOT_TYPE] = rt
        os.environ[const.PREFIX] = p

        counter = mocked_post(monkeypatch, endpoint, fs, fsp, ri, rt, v.strip() if v is not None else None)

        response = client.post('/web/', data=dict(move=v), follow_redirects=False)
        assert response.status_code == 302
        assert response.content_type == 'text/html; charset=utf-8'
        assert urlparse(response.location).path == os.path.join('/', p.strip(), 'web/')
        if v is not None and len(v.strip()) != 0:
            assert counter.count == 1
        else:
            assert counter.count == 0

    def test_raise_error(self, monkeypatch, endpoint, client):
        v = 'dummy'

        def mocked_post(endpoint, headers, data):
            raise requests.exceptions.RequestException()

        monkeypatch.setattr(requests, 'post', mocked_post)

        response = client.post('/web/', data=dict(move=v), follow_redirects=False)
        assert response.status_code == 500
        assert response.content_type == 'application/json'
        assert response.json == {'error': 'Internal Server Error'}

    @pytest.mark.parametrize('data', ['EMPTY', None, {'invalid': 'dummy'}])
    def test_bad_request(self, monkeypatch, endpoint, mocked_post, client, data):
        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', 'dummy')

        if data == 'EMPTY':
            response = client.post('/web/', follow_redirects=False)
        else:
            response = client.post('/web/', data=data, follow_redirects=False)
        assert response.status_code == 302
        assert response.content_type == 'text/html; charset=utf-8'
        assert urlparse(response.location).path == '/web/'
        assert counter.count == 0

    @pytest.mark.parametrize('method', ['get', 'post', 'head'])
    def test_moved_permanentry(self, monkeypatch, endpoint, mocked_post, client, method):
        v = 'dummy'

        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', v.strip() if v is not None else None)

        response = getattr(client, method)('/web', data=dict(move=v), follow_redirects=False)
        assert response.status_code == 301
        assert response.content_type == 'text/html; charset=utf-8'
        assert counter.count == 0

    @pytest.mark.parametrize('method', ['put', 'patch', 'delete'])
    @pytest.mark.parametrize('path', ['/web/', '/web'])
    def test_method_not_allowed(self, monkeypatch, endpoint, mocked_post, client, method, path):
        v = 'dummy'

        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', v.strip() if v is not None else None)

        response = getattr(client, method)(path, data=dict(move=v), follow_redirects=False)
        assert response.status_code == 405
        assert response.content_type == 'application/json'
        assert response.json == {'error': 'Method Not Allowed'}
        assert counter.count == 0


class TestNotFound:

    @pytest.mark.parametrize('method', ['get', 'post', 'put', 'patch', 'delete', 'head'])
    @pytest.mark.parametrize('path', ['/invalid/', '/invalid', ])
    def test_not_found(self, monkeypatch, endpoint, mocked_post, client, method, path):
        v = 'dummy'

        counter = mocked_post(monkeypatch, endpoint, '', '', '', '', v)

        data = {
            'data': [
                {
                    'button': {
                        'value': v,
                    },
                },
            ],
        }
        response = getattr(client, method)(path, data=json.dumps(data), content_type='application/json')
        assert response.status_code == 404
        assert response.content_type == 'application/json'
        if method != 'head':
            assert response.json == {'error': 'Not Found'}
        assert counter.count == 0
