# -*- coding: utf-8 -*-
import string
import random


def get_random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])
