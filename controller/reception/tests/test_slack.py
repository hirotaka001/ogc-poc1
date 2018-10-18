import unittest
from unittest import mock
from slack import send_message_to_slack
import requests


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
            if args[0] == 'url_200':
                return MockResponse(200)
            elif args[0] == 'url_400':
                return MockResponse(400)
            elif args[0] == 'url_403':
                return MockResponse(403)
            elif args[0] == 'url_404':
                return MockResponse(404)
            elif args[0] == 'url_410':
                return MockResponse(410)
            elif args[0] == 'url_500':
                return MockResponse(500)
            else:
                pass
        self.mock_post.side_effect = change_response
        r = send_message_to_slack('url_200', 'test')
        self.assertEqual(r.status_code, 200)
        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('url_400', 'test')
        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('url_403', 'test')
        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('url_404', 'test')
        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('url_410', 'test')
        with self.assertRaises(requests.exceptions.HTTPError):
            r = send_message_to_slack('url_500', 'test')
