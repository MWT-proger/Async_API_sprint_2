from http import HTTPStatus

import pytest
from functional.config import TestUrls
from functional.models.genre import Genre
from functional.utils.app_logger import get_logger

urls = TestUrls()
logger = get_logger('Test Genre')


@pytest.mark.asyncio
async def test_get_genres(make_get_request, genres_to_es, expected_genres):
    response = await make_get_request(urls.genres)

    assert response.status == HTTPStatus.OK
    assert response.body == expected_genres
    assert [Genre(**item) for item in response.body]


@pytest.mark.asyncio
async def test_get_genre_ok(make_get_request, genres_to_es):
    response = await make_get_request(urls.genres + "56b541ab-4d66-4021-8708-397762bff2d4")

    assert response.status == HTTPStatus.OK
    assert response.body == {
        "id": "56b541ab-4d66-4021-8708-397762bff2d4",
        "name": "Music"
    }


@pytest.mark.asyncio
async def test_get_genre_not_found(make_get_request, genres_to_es):
    response = await make_get_request(urls.genres + "63c24835-34d3-4279-8d81-3c5f4ddb0cdc4")

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == "genre not found"
