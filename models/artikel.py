from pydantic import BaseModel
from typing import Optional

class Artikel(BaseModel):
    headline: str
    shorttext: Optional[str] = None
    longtext: str

class ArtikelUpdate(BaseModel):
    headline: Optional[str] = None
    shorttext: Optional[str] = None
    longtext: Optional[str] = None