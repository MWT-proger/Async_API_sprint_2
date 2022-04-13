from functional.settings import TestSettings

settings = TestSettings()
BASE_URL_V1 = "{protocol}://{host}:{port}/api/v1".format(protocol=settings.service_protocol,
                                                         host=settings.service_host,
                                                         port=settings.service_port)


class TestUrls:
    search_films: str = BASE_URL_V1 + "/films/search/"
    films: str = BASE_URL_V1 + "/films/"
    genres: str = BASE_URL_V1 + "/genres/"
    persons: str = BASE_URL_V1 + "/persons/"
    search_persons: str = BASE_URL_V1 + "/persons/search/"


class TestFilesPath:
    films: str = "tests/functional/testdata/films.json"
    persons: str = "tests/functional/testdata/persons.json"
    genres: str = "tests/functional/testdata/genres.json"


class ElasticIndex:
    films: str = "movies"
    persons: str = "persons"
    genres: str = "genres"
