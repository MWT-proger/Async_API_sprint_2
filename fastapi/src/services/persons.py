from functools import lru_cache

from aioredis import Redis
from db.elastic import ElasticBase, ElasticService, get_elastic
from db.redis import RedisBase, RedisService, get_redis
from elasticsearch import AsyncElasticsearch
from models.person import PERSON_INDEX_ELASTIC, Person
from services.base import BaseService

from fastapi import Depends

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService(BaseService):
    index = PERSON_INDEX_ELASTIC
    model = Person

    def _get_search_request(self,
                            query_search=None,
                            **kwargs):
        return {"query": {"multi_match": {"query": query_search, "fuzziness": "auto", "fields": ["full_name"]}}} \
            if query_search else None

    def _get_key(self,
                 query_search=None,
                 page_size=50,
                 page_number=1,
                 **kwargs):
        return "query_search: %s, page_size:%s, page_number:%s" \
               % (query_search, page_size, page_number)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elasticsearch: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(RedisService(redis), ElasticService(elasticsearch))
