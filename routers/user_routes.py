from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from db.database import database, usertabelle
from models.user import User
from auth.security import hash_passwort, create_access_token, pwd_context, ACCESS_TOKEN_EXPIRE_MINUTEN, get_current_user
from typing import List


router = APIRouter()

# Registrieren
@router.post("/registrierung")
async def register(user: User):
    
    # PW hashen
    hashed_pw = hash_passwort(user.password)

    # Check ob user schon vorhanden
    query = usertabelle.select().where(usertabelle.c.email==user.email)
    existing_user = await database.fetch_one(query)

    if not existing_user:
    # DB Anfrage
        query = usertabelle.insert().values(
            email=user.email,
            password=hashed_pw,
            role=user.role
     )

    # DB Ausführung
        await database.execute(query)
        return {"message": "Benutzer erfolgreich angelegt!"}
    else:
        raise HTTPException(status_code=400, detail="User bereits registriert")

# Login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    # Check ob User existen
    query = usertabelle.select().where(usertabelle.c.email == form_data.username)
    found_user = await database.fetch_one(query)

    if not found_user:
        raise HTTPException(status_code=400, detail="User nicht gefunden")
    
    if not pwd_context.verify(form_data.password, found_user["password"]):
        raise HTTPException(status_code=400, detail="Passwort nicht korrekt")
    
    print("Gefundener Benutzer:", dict(found_user))
    
    # Token erzeugen
    access_token_expire = timedelta(ACCESS_TOKEN_EXPIRE_MINUTEN)
    access_token = create_access_token(
        data={
            "sub": found_user["email"],
            "role": found_user["role"]
        },
        expires_delta=access_token_expire
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/userlist", response_model=List[User])
async def get_users(current_user: str = Depends(get_current_user)):
    
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nicht berechtigt")

    query = usertabelle.select()
    userliste = await database.fetch_all(query)

    return [User(**dict(user)) for user in userliste]