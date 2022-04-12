from http import HTTPStatus

import pytest
from functional.config import TestUrls
from functional.models.genre import Genre, GENRES_INDEX_ELASTIC
from functional.utils.app_logger import get_logger

urls = TestUrls()
logger = get_logger('Test Genre')


@pytest.mark.asyncio
async def test_get_genres(make_get_request, redis_client, genres_to_es):
    response = await make_get_request(urls.genres)
    redis_body = await redis_client.get(index=GENRES_INDEX_ELASTIC, model=Genre)

    assert response.status == HTTPStatus.OK
    assert [Genre(**item) for item in response.body]
    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_genre_ok(make_get_request, redis_client):
    response = await make_get_request(urls.genres + "56b541ab-4d66-4021-8708-397762bff2d4")
    key = "56b541ab-4d66-4021-8708-397762bff2d4"
    redis_body = await redis_client.get(index=GENRES_INDEX_ELASTIC, key=key, model=Genre)

    assert response.status == HTTPStatus.OK
    assert response.body == {
        "id": "56b541ab-4d66-4021-8708-397762bff2d4",
        "name": "Music"
    }
    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_genre_not_found(make_get_request):
    response = await make_get_request(urls.genres + "63c24835-34d3-4279-8d81-3c5f4ddb0cdc4")

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == "genre not found"
