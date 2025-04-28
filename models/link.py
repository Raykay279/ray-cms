from pydantic import BaseModel
from typing import Optional

class Link(BaseModel):
    url = str
    clicktext = str

class LinkUpdate(BaseModel):
    url = Optional[str] = None
    clicktext = Optional[str] = None
