from http import HTTPStatus
from typing import List, Optional, Dict, Union

from pydantic import BaseModel

from fastapi import APIRouter, Query, Depends, HTTPException
from services.persons import PersonService, get_person_service

router = APIRouter()

OBJ_KEY = str
OBJ_VALUE = Optional[Union[float, str]]


class Person(BaseModel):
    id: str
    full_name: str
    films: List[Dict[OBJ_KEY, OBJ_VALUE]] = None


@router.get('/search', response_model=List[Person])
async def persons_search(
        query: Optional[str] = Query(None),
        page_number: int = Query(1, alias='page[number]', title='Номер страницы'),
        page_size: int = Query(20, alias='page[size]', title='Размер страницы'),
        person_service: PersonService = Depends(get_person_service)
) -> List[Person]:
    body = {'query': {'multi_match': {'query': query, "fuzziness": "auto", 'fields': ['full_name']}}} \
        if query else {'query': {'match_all': {}}}

    persons = await person_service.search_persons(
        body=body,
        page_size=page_size,
        page_number=page_size * page_number - page_size,
    )
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Persons not found.')
    return [Person.parse_obj(person) for person in persons]


@router.get('/{person_id}', response_model=Person)
async def person_detail(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found.')
    return Person.parse_obj(person)
