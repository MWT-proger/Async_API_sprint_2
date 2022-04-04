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
    async def _get(self, key: str):
        return await self.redis.get(key)

    @backoff.on_exception(backoff.expo, RedisError, max_time=10, factor=2)
    async def set(self, key: str, value: str, expire: int) -> None:
        await self.redis.set(key=key, value=value, expire=expire)

    async def get_data(self, index, dataclass, key=None):
        data = await self._get(f'{index}: {key}' if key else index)
        if not data:
            return None
        if isinstance(data := json.loads(data), list):
            return [dataclass.parse_raw(item) for item in data]
        else:
            return dataclass.parse_obj(data)
