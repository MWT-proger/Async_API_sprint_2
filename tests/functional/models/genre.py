from functional.models.new_base_model import NewBaseModel as BaseModel

GENRES_INDEX = "genres"
GENRES_LIST_SIZE = 100


class Genre(BaseModel):
    name: str
