# -*- coding: utf-8 -*-
import time

from common.redis_api import redis_cli

try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from threading import get_ident
    except ImportError:
        from _thread import get_ident


class RedisLock(object):
    def __init__(self):
        self.redis_cli = redis_cli

    def try_lock(self):
        return self.redis_cli.setnx('redis-lock', get_ident, time=30)

    def get_lock(self):
        counter = 0
        while True:
            if self.try_lock():
                return
            counter += 1
            if counter > 20:
                raise Exception('Get Lock Timeout')
            time.sleep(1)

    def release_lock(self):
        pass
