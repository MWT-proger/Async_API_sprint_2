import asyncio
import json
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest
from functional.models.new_base_model import NewBaseModel
from elasticsearch import AsyncElasticsearch
from functional.config import ElasticIndex, TestFilesPath
from functional.settings import TestSettings
from functional.utils.transform import raw_data_to_es
from multidict import CIMultiDictProxy

settings = TestSettings()
es_index = ElasticIndex()
test_data = TestFilesPath()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='{host}:{port}'.format(host=settings.es_host, port=settings.es_port))
    yield client
    await client.close()


class RedisService:
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def get(self, index, key=None, model=NewBaseModel):
        data = await self.redis.get(f'{index}: {key}' if key else index)
        if not data:
            return None
        if isinstance(data := json.loads(data), list):
            data = [json.loads(item) for item in data]
            return [model(**film) for film in data]
        else:
            return model.parse_obj(data)


@pytest.fixture(scope='session')
async def redis_client():
    client = await aioredis.create_redis_pool((settings.redis_host, settings.redis_port), minsize=10, maxsize=20)
    yield RedisService(client)
    await client.flushdb()
    client.close()


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


class ElasticORM:
    """Позволяет загружать данные в Elastic и удалять их"""

    def __init__(self, path_file: str, index: str, es_client: AsyncElasticsearch):
        self.path_file = path_file
        self.index = index
        self.es_client = es_client

    async def load_data(self):
        with open(self.path_file, 'r') as file:
            raw_data = json.load(file)
            data = raw_data_to_es(raw_data=raw_data, index=self.index)
        await self.es_client.bulk(body='\n'.join(data) + '\n', index=self.index, refresh=True)

    async def delete_data(self):
        await self.es_client.delete_by_query(
            body={
                "query": {
                    "match_all": {}
                }
            },
            index=self.index
        )


@pytest.fixture(scope='session')
async def films_to_es(es_client):
    es_orm = ElasticORM(path_file=test_data.films, index=es_index.films, es_client=es_client)
    await es_orm.load_data()
    yield
    await es_orm.delete_data()


@pytest.fixture(scope='session')
async def persons_to_es(es_client):
    es_orm = ElasticORM(path_file=test_data.persons, index=es_index.persons, es_client=es_client)
    await es_orm.load_data()
    yield
    await es_orm.delete_data()


@pytest.fixture(scope='session')
async def genres_to_es(es_client):
    es_orm = ElasticORM(path_file=test_data.genres, index=es_index.genres, es_client=es_client)
    await es_orm.load_data()
    yield
    await es_orm.delete_data()
