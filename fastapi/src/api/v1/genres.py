from http import HTTPStatus
from typing import List

from api import constant
from pydantic import BaseModel
from services.genres import GenreService, get_genre_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


class Genre(BaseModel):
    id: str
    name: str


@router.get('/{genre_id}', response_model=Genre)
async def genre_detail(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.GENRE_NOT_FOUND)
    return Genre(id=genre.id, name=genre.name)


@router.get('/', response_model=List[Genre])
async def genre_list(genre_service: GenreService = Depends(get_genre_service)) -> List[Genre]:
    genres = await genre_service.get_specific_data()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.GENRES_NOT_FOUND)
    return [Genre.parse_obj(genre) for genre in genres]
