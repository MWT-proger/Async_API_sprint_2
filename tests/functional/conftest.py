import asyncio
import aiohttp
import aioredis
import pytest
import json

from dataclasses import dataclass
from typing import Optional
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from functional.config import ElasticIndex, TestFilesPath
from functional.settings import TestSettings
from functional.utils.transform import raw_data_to_es
from functional.models.person import Person
from functional.models.film import FilmList
from functional.models.genre import Genre

settings = TestSettings()
es_index = ElasticIndex()
test_data = TestFilesPath()


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


@pytest.fixture
def expected_persons():
    with open(test_data.persons, 'r') as file:
        return [Person.parse_obj(item).dict() for item in json.load(file)]


@pytest.fixture
def expected_films():
    with open(test_data.films, 'r') as file:
        return [FilmList.parse_obj(item).dict() for item in json.load(file)]


@pytest.fixture
def expected_genres():
    with open(test_data.genres, 'r') as file:
        return [Genre.parse_obj(item).dict() for item in json.load(file)]
