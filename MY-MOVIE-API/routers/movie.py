from fastapi import APIRouter, Depends, Body, Path, Query, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from services.movie import MovieService
from schema.movie import Movie

movie_router = APIRouter()
Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    try:
        result = MovieService(db).get_movies()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    finally:
        db.close()

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    try:
        result = MovieService(db).get_movie(id)
        if not result:
            raise HTTPException(status_code=404, detail="Lo siento, no lo encontré 😓")
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    finally:
        db.close()

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category_and_year(category: str = Query(min_length=3, max_length=20)):
    db = Session()
    try:
        result = MovieService(db).get_movie_category(category)
        if not result:
            raise HTTPException(status_code=404, detail="Lo siento, no lo encontré 😓")
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    finally:
        db.close()

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    try:
        new_movie = MovieService(db).create_movie(movie)
        return JSONResponse(content={"message": "Se ha registrado la película🍿🎥", "movie_id": new_movie.id}, status_code=201)
    finally:
        db.close()

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    try:
        updated_movie = MovieService(db).update_movie(id, movie)
        if not updated_movie:
            return JSONResponse(status_code=404, content={"message": "Película no encontrada"})
        return JSONResponse(status_code=200, content={"message": "Se ha modificado la película", "movie_id": updated_movie.id})
    finally:
        db.close()

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    try:
        deleted_movie = MovieService(db).delete_movie(id)
        if not deleted_movie:
            return JSONResponse(status_code=404, content={"message": "Película no encontrada"})
        return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})
    finally:
        db.close()
