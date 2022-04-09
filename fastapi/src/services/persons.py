from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from db.elastic import ElasticBase, ElasticService, get_elastic
from db.redis import RedisBase, RedisService, get_redis
from elasticsearch import AsyncElasticsearch
from models.person import PERSON_INDEX_ELASTIC, Person
from services.base import BaseService
from tools.cacheable import cacheable

from fastapi import Depends

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService(BaseService):
    def __init__(self, redis: RedisBase, elasticsearch: RedisBase):
        self.redis = redis
        self.elasticsearch = elasticsearch
        self.key = None

    @cacheable(prefix=PERSON_INDEX_ELASTIC, cache_expire=PERSON_CACHE_EXPIRE_IN_SECONDS)
    async def get_by_id(self, person_id: str) -> Person:
        """Возвращает объект персоны"""
        person = await self.redis.get(PERSON_INDEX_ELASTIC, key=person_id)
        if not person:
            person = await self.elasticsearch.get_by_id(PERSON_INDEX_ELASTIC, key=person_id)
            if not person:
                return None
        return Person.parse_obj(person)

    @cacheable(prefix=PERSON_INDEX_ELASTIC, cache_expire=PERSON_CACHE_EXPIRE_IN_SECONDS)
    async def get_specific_data(self,
                                query_search: str = None,
                                page_size: int = 50,
                                page_number: int = 1,
                                ) -> Optional[List[Person]]:
        """Поиск персон по параметрам"""
        print('page', page_number)
        self.key = 'query_search: %s, page_size:%s, page_number:%s' \
                   % (query_search, page_size, page_number)
        persons = await self.redis.get(PERSON_INDEX_ELASTIC, key=self.key)
        if not persons:
            body = await self._get_search_request(query_search)
            persons = await self.elasticsearch.search_data(
                query=body,
                index=PERSON_INDEX_ELASTIC,
                size=page_size,
                number=page_number
            )
            if not persons:
                return None
        return [Person.parse_obj(person) for person in persons]

    async def _get_search_request(self, query) -> dict:
        return {'query': {'multi_match': {'query': query, "fuzziness": "auto", 'fields': ['full_name']}}} \
            if query else None


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elasticsearch: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(RedisService(redis), ElasticService(elasticsearch))
