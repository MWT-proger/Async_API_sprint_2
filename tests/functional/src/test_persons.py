from http import HTTPStatus

import pytest
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
