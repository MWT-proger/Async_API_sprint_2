from http import HTTPStatus

import pytest
from functional.config import TestFilesPath, TestUrls
from functional.models.film import MOVIES_INDEX, Film, FilmDetail, FilmList
from functional.utils import app_logger, get_data

urls = TestUrls()
test_data = TestFilesPath()
logger = app_logger.get_logger("Test Film")


async def get_key(query_search: str = None,
                  sort: str = None,
                  filter_genre: str = None,
                  page_size: int = 50,
                  page_number: int = 1,
                  ):
    key = "query_search: %s, sort:%s, filter_genre:%s, page_size:%s, page_number:%s" \
          % (query_search, sort, filter_genre, page_size, page_number)
    return key


@pytest.mark.asyncio
async def test_get_films(make_get_request, films_to_es, cache_client):
    response = await make_get_request(urls.films)
    key = await get_key()
    redis_body = await cache_client.get(MOVIES_INDEX, key=key, model=FilmList)

    assert response.status == HTTPStatus.OK
    assert response.body[0]["imdb_rating"] < response.body[-1]["imdb_rating"]

    assert response.body == redis_body


@pytest.mark.asyncio
async def test_search_detailed(make_get_request, cache_client, film_search_to_es):
    page_size = 7
    data_from_file = await get_data.from_file(test_data.film_search)
    film_search = data_from_file[0]

    response = await make_get_request(urls.search_films, {"query": film_search["title"], "page[size]": page_size, })

    key = await get_key(query_search=film_search["title"], page_size=page_size)
    redis_body = await cache_client.get(MOVIES_INDEX, key=key, model=FilmList)

    assert response.status == HTTPStatus.OK
    assert [FilmList(**film) for film in response.body]
    assert len(response.body) <= page_size
    assert response.body[0]["id"] == film_search["id"]

    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_films_sorted_desk(make_get_request, cache_client):
    response = await make_get_request(urls.films, {"sort": "-imdb_rating"})
    key = await get_key(sort="-imdb_rating")
    redis_body = await cache_client.get(MOVIES_INDEX, key=key, model=FilmList)

    assert response.status == HTTPStatus.OK
    assert response.body[0]["imdb_rating"] > response.body[-1]["imdb_rating"]

    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_films_filter_by_genre_ok(make_get_request, cache_client, film_by_genre_to_es):
    page_size = 2
    data_from_file = await get_data.from_file(test_data.film_by_genre)
    film_by_genre = data_from_file[0]

    response = await make_get_request(urls.films, {"filter[genre]": film_by_genre["genre"][0]["id"],
                                                   "page[size]": page_size})
    key = await get_key(filter_genre=film_by_genre["genre"][0]["id"], page_size=page_size)
    redis_body = await cache_client.get(MOVIES_INDEX, key=key, model=FilmList)

    assert response.status == HTTPStatus.OK
    assert [FilmList(**film) for film in response.body]

    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_films_filter_by_genre_not_found(make_get_request):
    response = await make_get_request(urls.films, {"filter[genre]": "some_id_genre"})

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == "films not found"


@pytest.mark.asyncio
async def test_get_film_by_id_ok(make_get_request, cache_client, film_by_id_to_es):
    data_from_file = await get_data.from_file(test_data.film_by_id)
    film_by_id = data_from_file[0]

    response = await make_get_request(urls.films + film_by_id["id"])
    key = film_by_id["id"]
    redis_body = await cache_client.get(MOVIES_INDEX, key=key, model=FilmDetail)

    assert response.status == HTTPStatus.OK
    assert FilmDetail(**response.body)
    assert response.body["title"] == film_by_id["title"]

    assert response.body == redis_body


@pytest.mark.asyncio
async def test_get_film_by_id_not_found(make_get_request):
    response = await make_get_request(urls.films + "some_id_film")

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body["detail"] == "film not found"
