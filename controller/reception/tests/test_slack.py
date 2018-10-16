# -*- coding: utf-8 -*-
import json
import os
from urllib.parse import urlparse

import pytest
from pyquery import PyQuery as pq

import requests

from src import slack, const

class TestSlackAPI:
    @pytest.mark.parametrize('webhook', ['https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'])
    def test_send_message_to_slack(self, webhook):　
        r = send_message_to_slack(webhook, "ProjectRoom 1")
        assert r.ok == True
        assert r.status_code == 200
