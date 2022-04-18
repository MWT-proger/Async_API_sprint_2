from functional.settings import TestSettings

settings = TestSettings()
BASE_URL_V1 = "{protocol}://{host}:{port}/api/v1".format(protocol=settings.service_protocol,
                                                         host=settings.service_host,
                                                         port=settings.service_port)
BASE_TEST_PATH = "tests/functional/testdata/"


class TestUrls:
    search_films: str = BASE_URL_V1 + "/films/search/"
    films: str = BASE_URL_V1 + "/films/"
    genres: str = BASE_URL_V1 + "/genres/"
    persons: str = BASE_URL_V1 + "/persons/"
    search_persons: str = BASE_URL_V1 + "/persons/search/"


class TestFilesPath:
    films: str = BASE_TEST_PATH + "films.json"
    film_by_id: str = BASE_TEST_PATH + "film_by_id.json"
    film_by_genre: str = BASE_TEST_PATH + "film_by_genre.json"
    film_search: str = BASE_TEST_PATH + "film_search.json"
    persons: str = BASE_TEST_PATH + "persons.json"
    person_by_id: str = BASE_TEST_PATH + "person_by_id.json"
    person_search: str = BASE_TEST_PATH + "person_search.json"
    genres: str = BASE_TEST_PATH + "genres.json"
    genre_by_id: str = BASE_TEST_PATH + "genre_by_id.json"


class ElasticIndex:
    films: str = "movies"
    persons: str = "persons"
    genres: str = "genres"
