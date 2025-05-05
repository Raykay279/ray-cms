from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Bild(BaseModel):
    id: Optional[int] = None
    path: str
    caption: str
    created_at : Optional[datetime] = None

    class Config:
        form_attributes = True

class BildCreate(BaseModel):
    path: str
    caption: str

class BildUpdate(BaseModel):
    path: Optional[str] = None
    caption: Optional[str] = None

    class Config:
        form_attributes = True