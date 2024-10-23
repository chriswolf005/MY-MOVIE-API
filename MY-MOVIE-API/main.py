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

app = FastAPI()
app.title = "My first app with FastAPI"
app.version = '0.01'

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

class User(BaseModel):
    email: str
    password: str

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

# Lista de películas
movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un planeta llamado Pandora viven los Na'vi, seres que...",
        "year": 2009,
        "rating": 7.8,
        "category": "Accion"
    },
    {
        "id": 2,
        "title": "Inception",
        "overview": "Un ladrón que roba secretos corporativos a través de la tecnología de sueño...",
        "year": 2010,
        "rating": 8.8,
        "category": "Ciencia Ficcion"
    },
    {
        "id": 3,
        "title": "The Dark Knight",
        "overview": "Cuando el Joker emerge de su misterioso pasado, siembra el caos en Gotham...",
        "year": 2008,
        "rating": 9.0,
        "category": "Accion"
    },
    {
        "id": 4,
        "title": "Interstellar",
        "overview": "Un equipo de exploradores viaja a través de un agujero de gusano en el espacio...",
        "year": 2014,
        "rating": 8.6,
        "category": "Aventura"
    },
    {
        "id": 5,
        "title": "The Matrix",
        "overview": "Un hacker aprende de misteriosos rebeldes la verdadera naturaleza de su realidad...",
        "year": 1999,
        "rating": 8.7,
        "category": "Ciencia Ficcion"
    },
    {
        "id": 6,
        "title": "Pulp Fiction",
        "overview": "Las vidas de dos matones, un boxeador, la esposa de un gánster y un par de bandidos...",
        "year": 1994,
        "rating": 8.9,
        "category": "Crimen"
    },
    {
        "id": 7,
        "title": "Shawshank",
        "overview": "Dos hombres encarcelados se forjan un vínculo a lo largo de varios años...",
        "year": 1994,
        "rating": 9.3,
        "category": "Drama"
    },
    {
        "id": 8,
        "title": "The Godfather",
        "overview": "El patriarca envejecido de una dinastía del crimen organizado traslada el control...",
        "year": 1972,
        "rating": 9.2,
        "category": "Crimen"
    },
    {
        "id": 9,
        "title": "Fight Club",
        "overview": "Un oficinista insomne y un fabricante de jabón descuidado forman un club de pelea...",
        "year": 1999,
        "rating": 8.8,
        "category": "Drama"
    },
    {
        "id": 10,
        "title": "Forrest Gump",
        "overview": "La presidencia de Kennedy y Johnson, los eventos de Vietnam, Watergate...",
        "year": 1994,
        "rating": 8.8,
        "category": "Drama"
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "root":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content={"token": token})

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    try:
        result = db.query(MovieModel).all()
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    finally:
        db.close()

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    try:
        result = db.query(MovieModel).filter(MovieModel.id == id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Lo siento, no lo encontré 😓")
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    finally:
        db.close() 
   
@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category_and_year(category: str = Query(min_length=3, max_length=20)):
    db = Session()
    try:
        result = db.query(MovieModel).filter(MovieModel.category == category).all()
        if not result:
            raise HTTPException(status_code=404, detail="Lo siento, no lo encontré 😓")
        return JSONResponse(status_code=200, content=jsonable_encoder(result))
    finally:
        db.close()
      
   
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

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
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

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict:
    db=Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404)
    db.delete()
    db.commit()    
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})