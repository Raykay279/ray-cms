from pydantic import BaseModel
from typing import Optional

class Artikel(BaseModel):
    id: Optional[int] = None
    headline: str
    shorttext: Optional[str] = None
    longtext: str

class ArtikelUpdate(BaseModel):
    id: int
    headline: Optional[str] = None
    shorttext: Optional[str] = None
    longtext: Optional[str] = None