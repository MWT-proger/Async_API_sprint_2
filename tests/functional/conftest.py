import aiohttp
import asyncio
import aioredis
import pytest

from typing import Optional
from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

from functional.settings import TestSettings

settings = TestSettings()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='{host}:{port}'.format(host=settings.es_host, port=settings.es_port))
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = await aioredis.create_redis_pool((settings.redis_host, settings.redis_port), minsize=10, maxsize=20)
    yield client
    await client.close()


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(url: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner
