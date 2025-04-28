from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from db.database import database, user
from models.user import User

router = APIRouter()

# Registrieren

