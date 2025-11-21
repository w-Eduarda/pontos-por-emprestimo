from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: Optional[str] = None
    condition: Optional[str] = "Bom"

class BookOut(BaseModel):
    id: int
    title: str
    author: Optional[str]
    condition: Optional[str]
    owner_id: int
    available: bool

    class Config:
        orm_mode = True
