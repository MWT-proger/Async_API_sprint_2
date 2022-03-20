from uuid import UUID
from typing import Union, Optional, List, Dict

from new_base_model import NewBaseModel as BaseModel


class Genre(BaseModel):
    name: str
    description: Optional[str] = None
