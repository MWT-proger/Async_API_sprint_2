from typing import Optional

from models.new_base_model import NewBaseModel as BaseModel


class Genre(BaseModel):
    name: str
    description: Optional[str] = None
