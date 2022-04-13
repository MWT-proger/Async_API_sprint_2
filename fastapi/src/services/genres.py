from functools import lru_cache

from aioredis import Redis
from db.elastic import ElasticBase, ElasticService, get_elastic
from db.redis import RedisBase, RedisService, get_redis
from elasticsearch import AsyncElasticsearch
from models.genre import GENRES_INDEX_ELASTIC, GENRES_LIST_SIZE, Genre
from services.base import BaseService

from fastapi import Depends

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService(BaseService):
    index = GENRES_INDEX_ELASTIC
    model = Genre

    def _get_search_request(self,
                            query_search=None,
                            sort=None,
                            filter_genre=None):
        return None

    def _get_key(self,
                 query_search=None,
                 sort=None,
                 filter_genre=None,
                 page_size=None,
                 page_number=None):
        return None


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(RedisService(redis), ElasticService(elastic))
