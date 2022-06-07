from pydantic import BaseModel
from typing import Optional

class Film(BaseModel):
    id: Optional[int]
    title: str
    year: int
    rented: bool = False