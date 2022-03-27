from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from models.person import Person, PERSON_INDEX_ELASTIC

from typing import List, Optional
from fastapi import Depends

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Person:
        """Возвращает объект персоны"""
        person = await self._get_person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[Person]:
        """Получает данные о персоне из Elastic"""
        try:
            doc = await self.elastic.get(PERSON_INDEX_ELASTIC, person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def _put_person_to_cache(self, person: Person) -> None:
        """Складывает данные о персоне в кэш"""
        await self.redis.set('person:{id}'.format(id=person.id), person.json(), expire=PERSON_CACHE_EXPIRE_IN_SECONDS)

    async def _get_person_from_cache(self, person_id):
        """Получает данные о персоне из кэша"""
        data = await self.redis.get(person_id)
        if not data:
            return None
        return Person.parse_raw(data)

    async def search_persons(self, body, page_size, page_number) -> Optional[List[Person]]:
        """Поиск персон по параметрам"""
        persons = await self._get_persons_from_elastic(body, page_size, page_number)
        if not persons:
            return None
        return persons

    async def _get_persons_from_elastic(self, body, page_size, page_number) -> List[Person]:
        """Получает данные о персонах из Elastic по параметрам"""
        persons = await self.elastic.search(
            index='persons',
            body=body,
            size=page_size,
            from_=page_number
        )
        return [Person(**person['_source']) for person in persons['hits']['hits']]


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elasticsearch: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(redis, elasticsearch)
