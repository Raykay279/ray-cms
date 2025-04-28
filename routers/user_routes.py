from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from auth.security import create_access_token, hash_passwort, pwd_context, ACCESS_TOKEN_EXPIRE_MINUTEN
from db.database import database, user_table
from datetime import timedelta

router = APIRouter()

# Benutzer registrierung
@router.post("/registrierung")
async def user_registrierung(user: User):
    hashed_passwort = hash_passwort(user.password)

    # SQL insert query vorbereiten
    query = user_table.insert().values(
        email=user.email,
        name=user.name,
        password=hashed_passwort,
    )

    await database.execute(query)

    return {"message": "Benutzer erfolgreich registriert"}

# Login Endpunkt
@router("/login")
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = user_table.select().where(user_table.c.email == form_data.email)
    angefragter_user = await database.fetch_one(query)

    if not angefragter_user;
        raise HTTPException(status_code=404, message="User nicht gefunden")
    
    if not pwd_context.verify(form_data.password, angefragter_user["password"]):
        raise HTTPException(status_code=400, message="Passwort falsch!")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTEN)

    acces_token = create_access_token(
        data={"sub": angefragter_user["email"]},
        expires_delta=access_token_expires
    )    

    return{"access_token": acces_token, "token_type": "bearer"}