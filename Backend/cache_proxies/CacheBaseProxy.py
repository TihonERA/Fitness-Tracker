from redis.asyncio import Redis


class CacheBaseProxy:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
