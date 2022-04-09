from http import HTTPStatus

import pytest
from functional.config import TestUrls
from functional.models.film import Film, FilmList
from functional.utils.app_logger import get_logger

urls = TestUrls()
logger = get_logger('Test Film')


@pytest.mark.asyncio
async def test_search_detailed(make_get_request, films_to_es):
    response = await make_get_request(urls.search_films, {'query': 'Star Was Born', 'page[size]': 7, })

    assert response.status == HTTPStatus.OK
    assert [FilmList(**film) for film in response.body]
    assert len(response.body) == 7
    assert response.body[0]['imdb_rating'] < response.body[-1]['imdb_rating']
    assert response.body[0]['id'] == '3f8873be-f6b1-4f3f-8a01-873924659851'


@pytest.mark.asyncio
async def test_get_films(make_get_request, expected_films):
    response = await make_get_request(urls.films)

    assert response.status == HTTPStatus.OK
    assert response.body == expected_films
    assert response.body[0]['imdb_rating'] < response.body[-1]['imdb_rating']


@pytest.mark.asyncio
async def test_get_films_sorted_desk(make_get_request, expected_films):
    response = await make_get_request(urls.films, {'sort': '-imdb_rating'})

    assert response.status == HTTPStatus.OK
    assert response.body[0]['imdb_rating'] > response.body[-1]['imdb_rating']


@pytest.mark.asyncio
async def test_get_films_filter_by_genre_ok(make_get_request):
    response = await make_get_request(urls.films, {'filter[genre]': '9c91a5b2-eb70-4889-8581-ebe427370edd',
                                                   'page[size]': 2, 'page[number]': 2})

    assert response.status == HTTPStatus.OK
    assert [FilmList(**film) for film in response.body]
    assert len(response.body) == 1
    assert response.body[0]['title'] == 'Amateur Porn Star Killer 3: The Final Chapter'


@pytest.mark.asyncio
async def test_get_films_filter_by_genre_not_found(make_get_request):
    response = await make_get_request(urls.films, {'filter[genre]': '237fd1e4-c98e-454e-aa13-8a13fb7547b5'})

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == "films not found"


@pytest.mark.asyncio
async def test_get_film_by_id_ok(make_get_request):
    response = await make_get_request(urls.films + "b9151ead-cf2f-4e14-aeb9-c4617f68848f")

    assert response.status == HTTPStatus.OK
    assert Film(**response.body)
    assert response.body['title'] == 'Star Quest: The Odyssey'


@pytest.mark.asyncio
async def test_get_film_by_id_not_found(make_get_request):
    response = await make_get_request(urls.films + "237fd1e4-c98e-454e-aa13-8a13fb7547b5")

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body['detail'] == "film not found"
