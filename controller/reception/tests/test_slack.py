import unittest
from unittest import mock
from src.slack import send_message_to_slack
import requests
import json


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def raise_for_status(self):
        if 400 <= self.status_code < 500:
            raise requests.exceptions.HTTPError('Client Error')
        elif 500 <= self.status_code < 600:
            raise requests.exceptions.HTTPError('Server Error')


class test_send_message_to_slack(unittest.TestCase):
    def setUp(self):
        self.patcher = mock.patch('slack.requests.post')
        self.mock_post = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_send_message_to_slack(self):
        def change_response(*args, **kwargs):
            if args[0] == 'http://url_200':
                return MockResponse(200)
            elif args[0] == 'http://url_400':
                return MockResponse(400)
            elif args[0] == 'http://url_403':
                return MockResponse(403)
            elif args[0] == 'http://url_404':
                return MockResponse(404)
            elif args[0] == 'http://url_410':
                return MockResponse(410)
            elif args[0] == 'http://url_500':
                return MockResponse(500)
            elif args[0] == 'http://service_not_known':
                raise requests.exceptions.ConnectionError('Failed to establish a new connection')
            else:
                raise requests.exceptions.MissingSchema('No schema supplied')
        self.mock_post.side_effect = change_response
        r = send_message_to_slack('http://url_200', 'ProjectRoom')
        self.assertEqual(r, 'ProjectRoom')

        r = send_message_to_slack('http://url_200', None)
        self.assertEqual(r, None)

        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('http://url_400', 'ProjectRoom 1')
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_400')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。TIS株式会社までご案内いたしております"

        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('http://url_403', 'ProjectRoom 1')
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_403')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。TIS株式会社までご案内いたしております"

        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('http://url_404', 'ProjectRoom 1')
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_404')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。TIS株式会社までご案内いたしております"

        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('http://url_410', 'ProjectRoom 1')
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_410')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。TIS株式会社までご案内いたしております"

        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('http://url_500', 'ProjectRoom 1')
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_500')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。TIS株式会社までご案内いたしております"

        with self.assertRaises(requests.exceptions.ConnectionError):
            r = send_message_to_slack('http://service_not_known', 'ProjectRoom 1')
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://service_not_known')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。TIS株式会社までご案内いたしております"

        with self.assertRaises(requests.exceptions.MissingSchema):
            r = send_message_to_slack('', 'ProjectRoom 1')
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], '')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。TIS株式会社までご案内いたしております"

        with self.assertRaises(requests.exceptions.MissingSchema):
            r = send_message_to_slack(None, 'ProjectRoom 1')
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], None)
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。TIS株式会社までご案内いたしております"

        r = send_message_to_slack('http://url_200', 'ProjectRoom 1')
        self.assertEqual(r.status_code, 200)
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_200')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。TIS株式会社までご案内いたしております"

        r = send_message_to_slack('http://url_200', 'dest 1-1')
        self.assertEqual(r.status_code, 200)
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_200')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。ホワイトボード室までご案内いたしております"

        r = send_message_to_slack('http://url_200', 'dest 1-2')
        self.assertEqual(r.status_code, 200)
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_200')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。会議室１までご案内いたしております"

        r = send_message_to_slack('http://url_200', 'dest 1-3')
        self.assertEqual(r.status_code, 200)
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_200')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。会議室２までご案内いたしております"

        r = send_message_to_slack('http://url_200', 'dest 1-4')
        self.assertEqual(r.status_code, 200)
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_200')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。会議室３までご案内いたしております"

        r = send_message_to_slack('http://url_200', 'dest 2-1')
        self.assertEqual(r.status_code, 200)
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_200')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。会津若松市　情報政策課までご案内いたしております"

        r = send_message_to_slack('http://url_200', 'dest 2-2')
        self.assertEqual(r.status_code, 200)
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_200')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。株式会社シンクまでご案内いたしております"

        r = send_message_to_slack('http://url_200', 'dest 2-3')
        self.assertEqual(r.status_code, 200)
        multi_args, multi_kwargs = self.mock_post.call_args
        self.assertEqual(multi_args[0], 'http://url_200')
        assert json.loads(multi_kwargs['data'])['text'] == "来客がいらっしゃいました。株式会社ソニックスまでご案内いたしております"
