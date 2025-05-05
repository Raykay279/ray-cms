from pydantic import BaseModel
from typing import Optional

class Link(BaseModel):
    id: Optional[int] = None
    url: str
    clicktext: str

    class Config:
        form_attributes = True

class LinkUpdate(BaseModel):
    url:Optional[str] = None
    clicktext: Optional[str] = None

    class Config:
        form_attributes = True

class LinkCreate(BaseModel):
    url: Optional[str] = None
    clicktext: Optional[str] = None

    class Config:
        form_attributes = True
