import json
from typing import Optional

import backoff
from aioredis import Redis, RedisError
from db.interfaces import RedisBase

redis: Optional[Redis] = None


async def get_redis() -> Redis:
    return redis


class RedisService(RedisBase):
    def __init__(self, redis: Redis):
        self.redis = redis

    @backoff.on_exception(backoff.expo, RedisError, max_time=10, factor=2)
    async def get(self, index, key=None):
        data = await self.redis.get(f'{index}: {key}' if key else index)
        if not data:
            return None
        return json.loads(data)

    @backoff.on_exception(backoff.expo, RedisError, max_time=10, factor=2)
    async def set(self, key: str, value: str, expire: int) -> None:
        await self.redis.set(key=key, value=value, expire=expire)
