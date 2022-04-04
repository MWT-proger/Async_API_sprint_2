from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):

    es_host: str = Field('host.docker.internal', env='ELASTIC_HOST')
    es_port: str = Field('9200', env='ELASTIC_PORT')

    redis_host: str = Field('host.docker.internal', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')

    service_protocol: str = Field('http', env='SERVICE_PROTOCOL')
    service_host: str = Field('host.docker.internal', env='SERVICE_HOST')
    service_port: str = Field('9000', env='SERVICE_PORT')


