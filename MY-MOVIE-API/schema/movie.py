from pydantic import BaseModel,Field
from typing import Optional,List

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
