from functional.settings import TestSettings

settings = TestSettings()
BASE_URL_V1 = '{protocol}://{host}:{port}/api/v1'.format(protocol=settings.service_protocol,
                                                         host=settings.service_host,
                                                         port=settings.service_port)


class TestUrls:
    search_films: str = BASE_URL_V1 + '/films/search/'
    films: str = BASE_URL_V1 + '/films/'


class ElasticIndex:
    films: str = 'movies'
    persons: str = 'persons'
    genres: str = 'genres'
