import json
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from models.genre import Genre, GENRES_INDEX_ELASTIC, GENRES_LIST_SIZE

from fastapi import Depends

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, redis: Redis, elasticsearch: AsyncElasticsearch):
        self.redis = redis
        self.elasticsearch = elasticsearch

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        """Получает жанр по id"""
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def get_all(self) -> Optional[List[Genre]]:
        """Получает список жанров"""
        genres = await self._get_all_genres_from_cache()
        if not genres:
            genres = await self._get_genres_from_elastic()
            if not genres:
                return None
            await self._put_genres_to_cache(genres)
        return genres

    async def _get_genres_from_elastic(self) -> List[Genre]:
        genres = await self.elasticsearch.search(
            body={"query": {"match_all": {}}},
            index='genres',
            size=GENRES_LIST_SIZE)
        return [Genre(**genre['_source']) for genre in genres['hits']['hits']]

    async def _put_genres_to_cache(self, genres: List[Genre]) -> None:
        await self.redis.set(
            'genres',
            json.dumps([genre.json() for genre in genres]),
            expire=GENRE_CACHE_EXPIRE_IN_SECONDS
        )

    async def _get_all_genres_from_cache(self) -> Optional[List[Genre]]:
        data = await self.redis.get('genres')
        if not data:
            return None
        genres = [Genre.parse_raw(item) for item in json.loads(data)]
        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elasticsearch.get(GENRES_INDEX_ELASTIC, genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _genre_from_cache(self, genre_id: str):
        """Получает данные о жанре из кэша"""
        data = await self.redis.get("%s:" % GENRES_INDEX_ELASTIC + genre_id)
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        """Складывает данные о жанре в кэш"""
        await self.redis.set("%s:" % GENRES_INDEX_ELASTIC + genre.id, genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(redis, elastic)
