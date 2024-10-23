from fastapi import APIRouter
from fastapi import FastAPI, Depends, Body, Path, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler

movie_router=APIRouter()

class Movie(BaseModel):
    id: Optional[int]=None
    title: str = Field(min_length=1, max_length=50)
    overview: str = Field(min_length=15, max_length=200)
    year: int = Field(le=2024)
    rating: Optional[float] = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=20)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2024,
                "rating": 1.8,
                "category": "Accion",
            }
        }


@movie_router.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@movie_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "root":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content={"token": token})

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    try:
        result = db.query(MovieModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    finally:
        db.close()

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    try:
        result = db.query(MovieModel).filter(MovieModel.id == id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Lo siento, no lo encontré 😓")
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    finally:
        db.close() 
   
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category_and_year(category: str = Query(min_length=3, max_length=20)):
    db = Session()
    try:
        result = db.query(MovieModel).filter(MovieModel.category == category).all()
        if not result:
            raise HTTPException(status_code=404, detail="Lo siento, no lo encontré 😓")
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    finally:
        db.close()
      
@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)  
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump(exclude_unset=True))
    try:
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)

        created_movie = Movie(
            id=new_movie.id,
            title=new_movie.title,
            overview=new_movie.overview,
            year=new_movie.year,
            rating=new_movie.rating,
            category=new_movie.category,
        )

        return JSONResponse(content={"message": "Se ha registrado la película🍿🎥", "movie_id": new_movie.id}, status_code=201)
    finally:
        db.close() 

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    try:
        result = db.query(MovieModel).filter(MovieModel.id == id).first()
        if not result:
            return JSONResponse(status_code=404, content={"message": "Película no encontrada"})
        
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category

        db.commit()
        db.refresh(result)
        
        return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db=Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404)
    db.delete()
    db.commit()    
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})