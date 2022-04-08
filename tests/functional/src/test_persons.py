import pytest
from http import HTTPStatus

from functional.config import TestUrls
from functional.models.person import Person
from functional.utils.app_logger import get_logger

urls = TestUrls()
logger = get_logger('Test Person')


@pytest.mark.asyncio
async def test_get_persons(make_get_request, persons_to_es, expected_persons):
    response = await make_get_request(urls.search_persons)

    assert response.status == HTTPStatus.OK
    assert response.body == expected_persons
    assert [Person(**item) for item in response.body]


# @pytest.mark.asyncio
# async def test_get_persons_page_size(make_get_request, persons_to_es, expected_persons):
#     response = await make_get_request(urls.search_persons, {'page[size]': 2, 'page[number]': 3})
#
#     assert response.status == HTTPStatus.OK
#     assert [Person(**item) for item in response.body]
#     assert len(response.body) == 1


@pytest.mark.asyncio
async def test_get_person_ok(make_get_request, persons_to_es):
    response = await make_get_request(urls.persons + "e039eedf-4daf-452a-bf92-a0085c68e156")

    assert response.status == HTTPStatus.OK
    assert Person(**response.body)
    assert response.body['full_name'] == 'Peter Cushing'


@pytest.mark.asyncio
async def test_get_person_not_found(make_get_request, persons_to_es):
    response = await make_get_request(urls.persons + "63c24835-34d3-4279-8d81-3c5f4ddb0cdc4")

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == "person not found"


@pytest.mark.asyncio
async def test_search_persons_ok(make_get_request, persons_to_es):
    response = await make_get_request(urls.search_persons, {'query': 'Luc'})

    assert response.status == HTTPStatus.OK
    assert [Person(**item) for item in response.body]
    logger.info(response.body)
    assert len(response.body) == 1
    assert response.body[0]['id'] == 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a'


@pytest.mark.asyncio
async def test_search_persons_ok_not_found(make_get_request, persons_to_es):
    response = await make_get_request(urls.search_persons, {'query': 'Makar'})

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == "persons not found"
