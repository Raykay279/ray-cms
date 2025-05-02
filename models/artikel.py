from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Artikel(BaseModel):
    id: Optional[int] = None
    headline: str
    shorttext: Optional[str] = None
    longtext: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class ArtikelUpdate(BaseModel):
    id: Optional[int] = None
    headline: Optional[str] = None
    shorttext: Optional[str] = None
    longtext: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True