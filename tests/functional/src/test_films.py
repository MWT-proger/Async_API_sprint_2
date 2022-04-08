import pytest
from http import HTTPStatus

from functional.config import TestUrls
from functional.models.film import FilmList
from functional.utils.app_logger import get_logger

urls = TestUrls()
logger = get_logger('Test Film')


@pytest.mark.asyncio
async def test_search_detailed(make_get_request, films_to_es):
    response = await make_get_request(urls.search_films, {'query': 'Star Was Born', 'page[size]': 1, })

    assert response.status == HTTPStatus.OK
    assert [FilmList(**film) for film in response.body]
    assert len(response.body) == 1


@pytest.mark.asyncio
async def test_get_films(make_get_request, expected_films):
    response = await make_get_request(urls.films)

    assert response.status == HTTPStatus.OK
    assert response.body == expected_films
