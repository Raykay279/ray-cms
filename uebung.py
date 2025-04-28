from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from db.database import database, user_table
from models.user import User
from auth.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTEN, pwd_context, hash_passwort

router = APIRouter()

#Registrieren
@router.post("login")

#Passwort hashen
async def benutzer_registrieren(user: User);
    hashed_pw = hash_passwort.hash(user.password)

#User anlegen
    query = user_table.inser().values(
        email=user.email,
        passwort=hashed_pw,
        name=user.name
    )

    await database.execute(query)

    return {"message": "Angekommen"}

# User login
@router.post("/login")
async def user_login(user_form: OAuth2PasswordRequestForm, Depends()):
    query = user_table.select().where(user_form.email == user_table.c.email)
    user = await database.fetch(query)