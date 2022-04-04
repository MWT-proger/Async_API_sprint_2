from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from db.elastic import ElasticBase, ElasticService, get_elastic
from db.redis import RedisBase, RedisService, get_redis
from elasticsearch import AsyncElasticsearch
from models.genre import GENRES_INDEX_ELASTIC, GENRES_LIST_SIZE, Genre
from services.base import BaseService
from tools.cacheable import cacheable

from fastapi import Depends

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService(BaseService):
    def __init__(self, redis: RedisBase, elasticsearch: ElasticBase):
        self.redis = redis
        self.elasticsearch = elasticsearch

    @cacheable(prefix=GENRES_INDEX_ELASTIC, cache_expire=GENRE_CACHE_EXPIRE_IN_SECONDS)
    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        """Получает жанр по id"""
        genre = await self.redis.get(GENRES_INDEX_ELASTIC, key=genre_id)
        if not genre:
            genre = await self.elasticsearch.get_by_id(GENRES_INDEX_ELASTIC, key=genre_id)
            if not genre:
                return None
        return Genre.parse_obj(genre)

    @cacheable(prefix=GENRES_INDEX_ELASTIC, cache_expire=GENRE_CACHE_EXPIRE_IN_SECONDS)
    async def get_specific_data(self) -> Optional[List[Genre]]:
        """Получает список жанров"""
        genres = await self.redis.get(GENRES_INDEX_ELASTIC, Genre)
        if not genres:
            genres = await self.elasticsearch.search_data(index=GENRES_INDEX_ELASTIC)
            if not genres:
                return None
        print(genres)
        return [Genre.parse_obj(genre) for genre in genres]


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(RedisService(redis), ElasticService(elastic))
