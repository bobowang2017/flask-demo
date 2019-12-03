# -*- coding: utf-8 -*-
import time

from common.redis_api import redis_cli

# try:
#     from greenlet import getcurrent as get_ident
# except ImportError:
#     try:
#         from threading import get_ident
#     except ImportError:
#         from _thread import get_ident
from threading import get_ident


class RedisLock(object):
    def __init__(self):
        self.redis_cli = redis_cli

    def try_lock(self):
        res = self.redis_cli.setnx('redis-lock', get_ident(), time=30)
        return True if res else False

    def get_lock(self):
        counter = 0
        # TODO 设置一个等待时间，百度去
        while True:
            if self.try_lock():
                return
            counter += 1
            if counter > 20:
                raise Exception('Get Lock Timeout')
            time.sleep(0.01)

    def release_lock(self):
        # 利用lua脚本解锁，保证下面的三个操作是一个原子
        lua = """      
        if  redis.call('get', KEYS[1]) == ARGV[1] 
            then
                return redis.call('del', KEYS[1])
            else
                return 0           
        end
        """
        self.redis_cli.register_script(lua, ['redis-lock'], [get_ident()])
