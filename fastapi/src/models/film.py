from typing import Dict, List, Optional, Union
from uuid import UUID

from models.new_base_model import NewBaseModel as BaseModel

OBJ_ID = Union[str, str, UUID]
OBJ_NAME = Union[str, str, UUID]

MOVIES_INDEX_ELASTIC = 'movies'


class Film(BaseModel):
    imdb_rating: Optional[float] = None
    genre: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    title: str
    description: Optional[str] = None
    director: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    actors_names: Optional[List[str]] = None
    writers_names: Optional[List[str]] = None
    actors: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    writers: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None


class FilmDetail(BaseModel):
    title: str
    imdb_rating: Optional[float] = None
    description: Optional[str] = None
    genre: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    actors: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    writers: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None
    directors: Optional[List[Dict[OBJ_ID, OBJ_NAME]]] = None


class FilmList(BaseModel):
    title: str
    imdb_rating: Optional[float] = None


data = [Film(id='3f8873be-f6b1-4f3f-8a01-873924659851', imdb_rating=1.0, genre=[{'id': '56b541ab-4d66-4021-8708-397762bff2d4', 'name': 'Music'}, {'id': '6d141ad2-d407-4252-bda4-95590aaf062a', 'name': 'Documentary'}], title='Justin Bieber: A Star Was Born', description=None, director=None, actors_names=['Justin Bieber'], writers_names=None, actors=[{'id': 'a967bacf-35ca-42ef-9bfd-3d003a957125', 'name': 'Justin Bieber'}], writers=None), Film(id='b9151ead-cf2f-4e14-aeb9-c4617f68848f', imdb_rating=1.5, genre=[{'id':'6c162475-c7ed-4461-9184-001ef3d9f26e', 'name': 'Sci-Fi'}], title='Star Quest: The Odyssey', description="As our world expands to include the entire galaxy everyone rushes to claim their own piece of this new world and thousands of colonies arise. With no core government, rogue colonies begin to wreak havoc and without a centralized army to protect the innocent peace is all but lost. Now at the end of mankind's greatest battle, empires will crumble, alliances will form, enemies will rise, and heroes will fall.", director=[{'id': 'bfbc0095-4b95-49e5-b72e-3e477f4e736c', 'name': 'Jon Bonnell'}], actors_names=['Aaron Ginn-Forsberg', 'Davina Joy', 'James Ray', 'Tamara McDaniel'], writers_names=['Carlos Perez', 'Ted Chalmers'], actors=[{'id': '4959e5b7-d157-4cdf-bc4f-5eb3cf8bd57f', 'name':'Aaron Ginn-Forsberg'}, {'id': '4f27971e-c80a-4894-be67-721fe7ff6a7f', 'name': 'Davina Joy'}, {'id': '571bc9f9-83ab-44f6-92e4-ec6e47772765', 'name': 'Tamara McDaniel'}, {'id': 'ddc8d633-79d5-4313-ad44-45e2ece6602b', 'name': 'James Ray'}], writers=[{'id': 'c4eb46cf-da3c-43ac-9b03-52430cf764ea', 'name': 'Ted Chalmers'}, {'id': 'f284b780-368c-4c60-8d9e-77328cbc0bae', 'name': 'Carlos Perez'}])]
print(isinstance(data, list))