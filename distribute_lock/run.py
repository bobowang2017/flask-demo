import os
import threading
import time

from common.redis_api import redis_cli
from distribute_lock.lock import RedisLock

redis_lock = RedisLock()

tickit = 5000


def sale(thread_name):
    global tickit
    global redis_lock
    while tickit > 0:
        if redis_lock.get_lock():
            if tickit > 0:
                tickit -= 1
                print('thread_name=%s 剩余tickit=%s' % (thread_name, tickit))
            else:
                print('票卖完了')
                os._exit(0)
            redis_lock.release_lock()
        time.sleep(1)


class MyThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = '线程' + str(name)

    def run(self) -> None:
        sale(self.name)


if __name__ == '__main__':
    for i in range(20):
        thread = MyThread(i)
        thread.start()
