import asyncio
from http import HTTPStatus

import pytest
from functional.config import TestUrls
from functional.models.person import Person, PERSON_INDEX_ELASTIC
from functional.utils.app_logger import get_logger

urls = TestUrls()
logger = get_logger('Test Person')


async def get_key(
        query_search: str = None,
        page_size: int = 20,
        page_number: int = 1
):
    key = 'query_search: %s, page_size:%s, page_number:%s' \
          % (query_search, page_size, page_number)
    return key


@pytest.mark.asyncio
async def test_get_persons(make_get_request, persons_to_es, redis_client):
    response = await make_get_request(urls.search_persons)
    key = await get_key()
    redis_body = await redis_client.get(PERSON_INDEX_ELASTIC, key=key, model=Person)

    assert response.status == HTTPStatus.OK
    assert [Person(**item) for item in response.body]
    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_persons_page_size(make_get_request, redis_client):
    response = await make_get_request(urls.search_persons, {'page[size]': 2, 'page[number]': 3})
    key = await get_key(page_size=2, page_number=3)
    redis_body = await redis_client.get(PERSON_INDEX_ELASTIC, key=key, model=Person)

    assert response.status == HTTPStatus.OK
    assert [Person(**item) for item in response.body]
    assert len(response.body) == 1
    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_person_ok(make_get_request, redis_client):
    response = await make_get_request(urls.persons + "e039eedf-4daf-452a-bf92-a0085c68e156")
    key = "e039eedf-4daf-452a-bf92-a0085c68e156"
    redis_body = await redis_client.get(PERSON_INDEX_ELASTIC, key=key, model=Person)

    assert response.status == HTTPStatus.OK
    assert Person(**response.body)
    assert response.body['full_name'] == 'Peter Cushing'
    assert redis_body == response.body


@pytest.mark.asyncio
async def test_get_person_not_found(make_get_request):
    response = await make_get_request(urls.persons + "63c24835-34d3-4279-8d81-3c5f4ddb0cdc4")

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == "person not found"


@pytest.mark.asyncio
async def test_search_persons_ok(make_get_request, redis_client):
    response = await make_get_request(urls.search_persons, {'query': 'Lucas'})
    key = await get_key(query_search='Lucas')
    redis_body = await redis_client.get(PERSON_INDEX_ELASTIC, key=key, model=Person)

    assert response.status == HTTPStatus.OK
    assert [Person(**item) for item in response.body]
    logger.info(response.body)
    assert len(response.body) == 1
    assert response.body[0]['id'] == 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a'
    assert redis_body == response.body


@pytest.mark.asyncio
async def test_search_persons_ok_not_found(make_get_request):
    response = await make_get_request(urls.search_persons, {'query': 'Makar'})

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == "persons not found"
