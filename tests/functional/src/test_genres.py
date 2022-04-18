from http import HTTPStatus

import pytest
from functional.config import TestUrls, TestFilesPath
from functional.models.genre import GENRES_INDEX, Genre
from functional.utils import app_logger, get_data

urls = TestUrls()
test_data = TestFilesPath()
logger = app_logger.get_logger("Test Genre")


@pytest.mark.asyncio
async def test_get_genres(make_get_request, redis_client, genres_to_es):
    response = await make_get_request(urls.genres)
    redis_body = await redis_client.get(index=GENRES_INDEX, model=Genre)

    assert response.status == HTTPStatus.OK
    assert [Genre(**item) for item in response.body]
    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_genre_ok(make_get_request, redis_client, genre_by_id_to_es):
    data_from_file = await get_data.from_file(test_data.genre_by_id)
    genre_by_id = data_from_file[0]

    response = await make_get_request(urls.genres + genre_by_id["id"])

    key = genre_by_id["id"]
    redis_body = await redis_client.get(index=GENRES_INDEX, key=key, model=Genre)

    assert response.status == HTTPStatus.OK
    assert response.body["id"] == genre_by_id["id"]
    assert response.body["name"] == genre_by_id["name"]
    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_genre_not_found(make_get_request):
    response = await make_get_request(urls.genres + "some_id_genre")

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == "genre not found"
