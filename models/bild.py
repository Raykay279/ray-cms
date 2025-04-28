from pydantic import BaseModel
from typing import Optional

class Bild(BaseModel):
    path: str
    caption: str

class BildUpdate(BaseModel):
    path: Optional[str] = None
    caption: Optional[str] = None
    