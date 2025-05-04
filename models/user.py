from pydantic import BaseModel, Field
from enum import Enum

class UserRole(str, Enum):
    viewer = "viewer"
    editor = "editor"
    admin = "admin"

class User(BaseModel):
    email: str
    password: str
    role: UserRole = Field(default=UserRole.viewer, description="Rolle des Nutzers")