from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from services.films import FilmService, get_film_service
from models.film import FilmDetail, FilmList
from api import constant

router = APIRouter()


@router.get('/{film_id}', response_model=FilmDetail)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDetail:
    """ Возвращает информацию по фильму с указанным id """
    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.FILM_NOT_FOUND)

    return FilmDetail(
        id=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=film.genre,
        actors=film.actors,
        writers=film.writers,
        directors=film.director)


@router.get('/', response_model=List[FilmList])
async def film_list(sort: Optional[str] = Query(None, alias = "sort"),
                    filter_genre: Optional[str] = Query(None, alias = "filter[genre]"),
                    page_number: int = Query(1, alias = 'page[number]', title = constant.TITLE_PAGE_NUMBER),
                    page_size: int = Query(50, alias = 'page[size]', title = constant.TITLE_PAGE_SIZE),
                    film_service: FilmService = Depends(get_film_service)) -> List[FilmList]:
    """ Возвращает информацию по фильмам"""
    films = await film_service.get_specific_film_list(
        sort=sort,
        filter_genre=filter_genre,
        page_size=page_size,
        page_number=page_number
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.FILMS_NOT_FOUND)
    return films


@router.get('/search/', response_model=List[FilmList])
async def film_list_search(query: Optional[str] = Query(None, alias = "query"),
                           page_number: int = Query(1, alias = 'page[number]', title = constant.TITLE_PAGE_NUMBER),
                           page_size: int = Query(50, alias = 'page[size]', title = constant.TITLE_PAGE_SIZE),
                           film_service: FilmService = Depends(get_film_service)) -> List[FilmList]:
    """ Возвращает информацию по фильмам """
    films = await film_service.get_specific_film_list(
        query_search=query,
        page_size=page_size,
        page_number=page_number
    )
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=constant.FILMS_NOT_FOUND)
    return films
