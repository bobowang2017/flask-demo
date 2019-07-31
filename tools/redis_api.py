import redis
redis_valid_time = 60 * 60


class RedisClient:
    def __init__(self):
        self.host = "redis-svc"
        self.port = "6379"

    @property
    def redis_client(self):
        client = redis.Redis(host=self.host, port=self.port)
        return client

    def get_instance(self, key, delete_cache=False):
        redis_instance = self.redis_client.get(key)
        if not redis_instance:
            return None
        try:
            res = eval(redis_instance)
        except:
            res = str(redis_instance, encoding='utf-8')
        if delete_cache:
            self.redis_client.delete(key)
        return res

    def set_instance(self, key, value, default_valid_time=redis_valid_time):
        self.redis_client.set(key, value, default_valid_time)
        return

    def delete(self, key):
        return self.redis_client.delete(key)

    def incr_instance(self, key, amount=1):
        return self.redis_client.incr(key, amount)

    def decr_instance(self, key, amount=1):
        return self.redis_client.decr(key, amount)

    def sadd(self, name, *value):
        """根据key添加数据到集合set（set类型数据操作）"""
        return self.redis_client.sadd(name, *value)

    def sismember(self, name, value):
        """判断集合name中是否存在value元素（set类型数据操作）"""
        return self.redis_client.sismember(name, value)


redis_cli = RedisClient()
