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
        form_attributes = True


class ArtikelCreate(BaseModel):
    headline: str
    shorttext: Optional[str] = None
    longtext: str


class ArtikelUpdate(BaseModel):
    headline: Optional[str] = None
    shorttext: Optional[str] = None
    longtext: Optional[str] = None

    class Config:
        form_attributes = True