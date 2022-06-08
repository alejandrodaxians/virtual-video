from pydantic import BaseModel, Field
from typing import Optional

class Film(BaseModel):
    id: Optional[int]
    title: str
    year: int
    rented: bool = False

class FilmUpdate(BaseModel):
    title: Optional[str]
    year: Optional[int]