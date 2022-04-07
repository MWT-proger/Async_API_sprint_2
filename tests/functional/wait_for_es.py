from time import sleep

from elasticsearch import Elasticsearch

from settings import TestSettings
from utils.app_logger import get_logger


settings = TestSettings()
logger = get_logger('Elasticsearch connection')


def wait_for_elastic():
    logger.info("start")

    elastic = Elasticsearch(hosts=[f'{settings.es_host}:{settings.es_port}'])

    while not elastic.ping():
        logger.error("connection error!")
        sleep(1)

    logger.info("successful connection!")


if __name__ == '__main__':
    wait_for_elastic()
