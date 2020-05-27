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
        # TODO 设置一个等待时间，百度去，超时后返回false
        while True:
            if self.try_lock():
                return True
            time.sleep(0.1)
            counter += 1
            if counter > 100:
                print('try get lock %s times' % counter)
            if counter > 200:
                return False

    def release_lock(self):
        # 利用lua脚本解锁，保证下面的三个操作是一个原子
        # 主要是怕误将其他客户端的锁解开。比如客户端A加锁，一段时间之后客户端A解锁，在进入unlock后执行jedis.del()
        # 之前，锁突然过期了，此时客户端B尝试加锁成功，然后客户端A再执行del()方法，则将客户端B的锁给解除。
        lua = """      
        if  redis.call('get', KEYS[1]) == ARGV[1] 
            then
                return redis.call('del', KEYS[1])
            else
                return 0           
        end
        """
        self.redis_cli.register_script(lua, ['redis-lock'], [get_ident()])
        print('==========================release lock')
