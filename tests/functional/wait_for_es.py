from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from settings import TestSettings
from utils.app_logger import get_logger
from utils.backoff import backoff

settings = TestSettings()
logger = get_logger('Elasticsearch connection')


@backoff()
def wait_for_elastic():
    logger.info("start")

    elastic = Elasticsearch(hosts=[f'{settings.es_host}:{settings.es_port}'], verify_certs=True)

    if not elastic.ping():
        raise ConnectionError

    logger.info("successful connection!")


if __name__ == "__main__":
    wait_for_elastic()
