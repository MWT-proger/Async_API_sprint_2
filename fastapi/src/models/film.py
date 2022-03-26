from typing import Dict, List, Optional, Union
from uuid import UUID

from new_base_model import NewBaseModel as BaseModel

OBJ_ID = Union[str, str, UUID]
OBJ_NAME = Union[str, str, UUID]


class Film(BaseModel):
    imdb_rating: Optional[float] = None
    genre: Optional[List[str]] = None
    title: str
    description: Optional[str] = None
    director: Optional[List[str]] = None
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    writers: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
