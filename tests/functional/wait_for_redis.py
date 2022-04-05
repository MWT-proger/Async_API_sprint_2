from time import sleep

from redis import ConnectionError, Redis
from settings import TestSettings

settings = TestSettings()


def wait_for_redis():
    redis = Redis(settings.redis_host)
    while True:
        try:
            redis.ping()
            print("Successful connect to redis")
            break
        except ConnectionError:
            print("Connection error!")
            sleep(1)


if __name__ == '__main__':
    wait_for_redis()
