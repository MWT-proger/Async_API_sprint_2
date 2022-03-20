from uuid import UUID
from typing import Union, Optional, List, Dict

from new_base_model import NewBaseModel as BaseModel


class Person(BaseModel):
    full_name: str
    birth_date: Optional[date] = None
    role: List[str] = None
    film_ids: List[str] = None
