from fastapi import FastAPI, Depends, Body, Path, Query, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from utils.jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "My first app with FastAPI"
app.version = '0.01'

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

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


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

