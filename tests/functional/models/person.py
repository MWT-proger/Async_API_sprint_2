from typing import Dict, List, Optional, Union

from functional.models.new_base_model import NewBaseModel as BaseModel

OBJ_KEY = str
OBJ_VALUE = Optional[Union[float, str]]

PERSON_INDEX = "persons"


class Person(BaseModel):
    full_name: str
    films: List[Dict[OBJ_KEY, OBJ_VALUE]] = None
