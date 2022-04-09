from time import sleep

from redis import ConnectionError, Redis
from settings import TestSettings
from utils.app_logger import get_logger

settings = TestSettings()
logger = get_logger('Redis connection')


def wait_for_redis():
    logger.info("start")
    redis = Redis(settings.redis_host)
    while True:
        try:
            redis.ping()
            logger.info("successful connection!")
            break
        except ConnectionError:
            logger.error("connection error!")
            sleep(1)


if __name__ == '__main__':
    wait_for_redis()
