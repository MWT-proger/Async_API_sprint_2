from time import sleep

from elasticsearch import Elasticsearch
from settings import TestSettings

settings = TestSettings()


def wait_for_elastic():
    elastic = Elasticsearch(hosts=[f'{settings.es_host}:{settings.es_port}'])
    while not elastic.ping():
        print("Elasticsearch connection error!")
        sleep(1)
    print("Successful connect to elasticsearch")


if __name__ == '__main__':
    wait_for_elastic()
