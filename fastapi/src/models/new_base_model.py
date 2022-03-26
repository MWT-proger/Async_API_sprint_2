import orjson
from pydantic import BaseModel
from uuid import UUID
from typing import Union


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class NewBaseModel(BaseModel):
    id: Union[str, UUID]

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
