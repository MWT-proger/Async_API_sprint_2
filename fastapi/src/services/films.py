from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from db.elastic import ElasticBase, ElasticService, get_elastic
from db.redis import RedisBase, RedisService, get_redis
from elasticsearch import AsyncElasticsearch
from models.film import MOVIES_INDEX_ELASTIC, Film
from services.base import BaseService
from tools.cacheable import cacheable

from fastapi import Depends

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
FILMS_LIST_SIZE = 100


class FilmService(BaseService):
    def __init__(self, redis: RedisBase, elasticsearch: ElasticBase):
        self.redis = redis
        self.elasticsearch = elasticsearch
        self.key = None

    @cacheable(prefix=MOVIES_INDEX_ELASTIC, cache_expire=FILM_CACHE_EXPIRE_IN_SECONDS)
    async def get_specific_data(self,
                                query_search: str = None,
                                sort: str = None,
                                filter_genre: str = None,
                                page_size: int = 50,
                                page_number: int = 1,
                                ):
        self.key = 'query_search: %s, sort:%s, filter_genre:%s, page_size:%s, page_number:%s' \
                   % (query_search, sort, filter_genre, page_size, page_number)

        films = await self.redis.get(MOVIES_INDEX_ELASTIC, key=self.key)
        if not films:
            body = await self._get_search_request(query_search=query_search, sort=sort, filter_genre=filter_genre)
            films = await self.elasticsearch.search_data(
                query=body,
                index=MOVIES_INDEX_ELASTIC,
                size=page_size,
                number=page_number
            )
            if not films:
                return None
        return [Film.parse_obj(film) for film in films]

    @cacheable(prefix=MOVIES_INDEX_ELASTIC, cache_expire=FILM_CACHE_EXPIRE_IN_SECONDS)
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self.redis.get(MOVIES_INDEX_ELASTIC, key=film_id)

        if not film:
            film = await self.elasticsearch.get_by_id(MOVIES_INDEX_ELASTIC, key=film_id)
            if not film:
                return None
        return Film.parse_obj(film)

    async def _get_search_request(self, query_search: str = None, sort: str = None,
                                  filter_genre: str = None) -> dict:
        if query_search:
            body = {
                "query": {
                    "multi_match": {
                        "query": query_search,
                        "fuzziness": "auto",
                        "fields": [
                            "title",
                            "description",
                            "genre.name",
                            "actors_names",
                            "writers_names",
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


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(RedisService(redis), ElasticService(elastic))
