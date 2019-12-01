# -*- coding: utf-8 -*-
from common.redis_api import redis_cli


class RedisLock(object):
    def __init__(self):
        self.redis_cli = redis_cli

    def get_lock(self):
        self.redis_cli.setnx()
