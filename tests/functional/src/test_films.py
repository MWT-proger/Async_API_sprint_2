import pytest
from functional.urls import TestUrls

urls = TestUrls()


@pytest.mark.asyncio
async def test_search_detailed(es_client, make_get_request):
    # Заполнение данных для теста
    # await es_client.bulk(...)

    response = await make_get_request(urls.search_films, {'query': 'Star Wars', 'page[size]': 1, })

    # Проверка результата
    assert response.status == 200
    assert len(response.body) == 1

    # assert response.body == expected
