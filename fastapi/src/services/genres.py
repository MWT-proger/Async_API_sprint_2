import json
from functools import lru_cache
from typing import Optional, List

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis

from models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5
GENRES_LIST_SIZE = 100


class GenreService:
    def __init__(self, redis: Redis, elasticsearch: AsyncElasticsearch):
        self.redis = redis
        self.elasticsearch = elasticsearch

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def get_all(self):
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

    async def _get_genre_from_elastic(self, genre_id: str):
        try:
            doc = await self.elasticsearch.get('genres', genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _genre_from_cache(self, genre_id: str):
        data = await self.redis.get(genre_id)
        if not data:
            return None

        genre = Genre.parse_raw(data)
        return genre

    async def _put_genre_to_cache(self, genre: Genre):
        await self.redis.set(genre.id, genre.json(), expire=GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(redis, elastic)
