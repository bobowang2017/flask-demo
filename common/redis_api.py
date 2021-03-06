import redis

from common.message import msg_const
from exts import logger, config

redis_valid_time = 60 * 60


class RedisClient:
    def __init__(self):
        self.host = config.REDIS_HOST
        self.port = config.REDIS_PORT

    @property
    def redis_client(self):
        try:
            pool = redis.ConnectionPool(host=self.host, port=self.port, max_connections=10000)
            client = redis.StrictRedis(connection_pool=pool)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)
            return None
        else:
            return client

    def get(self, key):
        try:
            redis_instance = self.redis_client.get(key)
            if not redis_instance:
                return None
            try:
                res = eval(redis_instance)
            except:
                res = str(redis_instance, encoding='utf-8')
            return res
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)
            return None

    def set(self, key, value, default_valid_time=redis_valid_time):
        try:
            self.redis_client.set(key, value, default_valid_time)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)

    def setnx(self, key, value, time=5):
        try:
            return self.redis_client.set(key, value, ex=time, nx=True)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)

    def delete(self, key):
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)

    def incr_instance(self, key, amount=1):
        try:
            self.redis_client.incr(key, amount)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)

    def decr_instance(self, key, amount=1):
        try:
            self.redis_client.decr(key, amount)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)

    def m_get(self, keys):
        try:
            return self.redis_client.mget(keys)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)

    def m_set(self, **kwargs):
        try:
            return self.redis_client.mset(**kwargs)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)

    def expire_at(self, key, value):
        try:
            return self.redis_client.expireat(key, value)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)

    def register_script(self, script, keys, args):
        try:
            cmd = self.redis_client.register_script(script)
            return cmd(keys=keys, args=args)
        except Exception as e:
            logger.info(e)
            logger.error(msg_const.REDIS_CONNECTION_500)


redis_cli = RedisClient()
