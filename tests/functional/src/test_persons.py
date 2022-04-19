from http import HTTPStatus

import pytest
from functional.config import TestFilesPath, TestUrls
from functional.models.person import PERSON_INDEX, Person
from functional.utils import app_logger, get_data

test_data = TestFilesPath()
urls = TestUrls()
logger = app_logger.get_logger("Test Person")


async def get_key(
        query_search: str = None,
        page_size: int = 20,
        page_number: int = 1
):
    key = "query_search: %s, page_size:%s, page_number:%s" \
          % (query_search, page_size, page_number)
    return key


@pytest.mark.asyncio
async def test_get_persons(make_get_request, persons_to_es, redis_client):
    response = await make_get_request(urls.search_persons)
    key = await get_key()
    redis_body = await redis_client.get(PERSON_INDEX, key=key, model=Person)

    assert response.status == HTTPStatus.OK
    assert [Person(**item) for item in response.body]
    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_persons_page_size(make_get_request, redis_client):
    response = await make_get_request(urls.search_persons, {"page[size]": 2, "page[number]": 3})
    key = await get_key(page_size=2, page_number=3)
    redis_body = await redis_client.get(PERSON_INDEX, key=key, model=Person)

    assert response.status == HTTPStatus.OK
    assert [Person(**item) for item in response.body]
    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_person_ok(make_get_request, redis_client, person_by_id_to_es):
    data_from_file = await get_data.from_file(test_data.person_by_id)
    person__by_id = data_from_file[0]

    response = await make_get_request(urls.persons + person__by_id["id"])
    key = person__by_id["id"]
    redis_body = await redis_client.get(PERSON_INDEX, key=key, model=Person)

    assert response.status == HTTPStatus.OK
    assert Person(**response.body)
    assert response.body["full_name"] == person__by_id["full_name"]
    assert redis_body == response.body


@pytest.mark.asyncio
async def test_get_person_not_found(make_get_request):
    response = await make_get_request(urls.persons + "some_id_person")

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == "person not found"


@pytest.mark.asyncio
async def test_search_persons_ok(make_get_request, redis_client, person_search_to_es):
    data_from_file = await get_data.from_file(test_data.person_search)
    person_search = data_from_file[0]

    response = await make_get_request(urls.search_persons, {"query": person_search["full_name"]})

    key = await get_key(query_search=person_search["full_name"])
    redis_body = await redis_client.get(PERSON_INDEX, key=key, model=Person)

    assert response.status == HTTPStatus.OK
    assert [Person(**item) for item in response.body]
    assert response.body[0]["id"] == person_search["id"]

    assert redis_body == response.body


@pytest.mark.asyncio
async def test_search_persons_ok_not_found(make_get_request):
    response = await make_get_request(urls.search_persons, {"query": "Some Person Not Found"})

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == "persons not found"
