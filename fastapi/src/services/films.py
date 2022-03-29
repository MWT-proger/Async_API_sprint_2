import json
from functools import lru_cache
from typing import Optional, List

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, Query

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, MOVIES_INDEX_ELASTIC

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
FILMS_LIST_SIZE = 100


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_specific_film_list(self,
                                     query_search: str = None,
                                     sort: str = None,
                                     filter_genre: str = None,
                                     page_size: int = 50,
                                     page_number: int = 1,
                                     ):
        key = 'query_search: %s, sort:%s, filter_genre:%s, page_size:%s, page_number:%s' \
              % (query_search, sort, filter_genre, page_size, page_number)

        films = await self._get_specific_film_list_from_cache(key=key)
        if not films:
            body = await self._get_body_request_elastic(query_search=query_search, sort=sort, filter_genre=filter_genre)
            films = await self._get_films_from_elastic(body=body, page_size=page_size, page_number=page_number)
            if not films:
                return None
            await self._put_films_to_cache(films, key)
        return films

    async def _get_body_request_elastic(self, query_search: str = None, sort: str = None, filter_genre: str = None) -> dict:
        if query_search:
            body = {
                "query": {
                    "multi_match": {
                        "query": query_search,
                        "fuzziness": "auto",
                        "fields": [
                            "actors_names",
                            "writers_names",
                            "title",
                            "description",
                            "genre.name"
                        ]
                    }
                }
            }
        else:
            body = {"sort": [{"imdb_rating": "asc"}]}
        if sort:
            if sort == "-imdb_rating":
                body["sort"] = [{"imdb_rating": "desc"}]

        if filter_genre:
            body["query"] = {
                "nested": {
                    "path": "genre",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match": {
                                        "genre.id": filter_genre
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        return body

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)

        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get(MOVIES_INDEX_ELASTIC, film_id)
        except NotFoundError:
            return None
        return Film(**doc["_source"])

    async def _get_films_from_elastic(self,
                                      body: dict = None,
                                      page_size: int = None,
                                      page_number: int = None,) -> List[Film]:
        films = await self.elastic.search(
            body=body,
            index=MOVIES_INDEX_ELASTIC,
            size=page_size,
            from_=page_size * page_number - page_size)
        return [Film(**film["_source"]) for film in films["hits"]["hits"]]

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)

        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _get_specific_film_list_from_cache(self, key: str = None) -> Optional[List[Film]]:
        data = await self.redis.get("%s_%s" % (MOVIES_INDEX_ELASTIC, key))
        if not data:
            return None
        films = [Film.parse_raw(item) for item in json.loads(data)]
        return films

    async def _put_film_to_cache(self, film: Film):
        """Добавляет данные о фильм в кеш"""
        await self.redis.set("%s:" % MOVIES_INDEX_ELASTIC + film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_films_to_cache(self, films: List[Film], key: str) -> None:
        """Добавляет данные о списках фильмов в кеш"""
        await self.redis.set(
            "%s_%s" % (MOVIES_INDEX_ELASTIC, key),
            json.dumps([film.json() for film in films]),
            expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
