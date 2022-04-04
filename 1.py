from typing import Dict, List, Optional, Union
from uuid import UUID


OBJ_ID = Union[str, str, UUID]
OBJ_NAME = Union[str, str, UUID]

MOVIES_INDEX_ELASTIC = 'movies'


class Film:
    imdb_rating: Optional[float] = None




data = [Film(), Film()]
print(isinstance(data, list))