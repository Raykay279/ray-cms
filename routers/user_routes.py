from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from db.database import database, usertabelle
from models.user import User
from auth.security import hash_passwort, create_access_token, pwd_context, ACCESS_TOKEN_EXPIRE_MINUTEN

router = APIRouter()

# Registrieren
@router.post("/registrierung")
async def register(user: User):
    
    # PW hashen
    hashed_pw = hash_passwort(user.password)

    # DB Anfrage
    query = usertabelle.insert().values(
        name=user.name,
        email=user.email,
        password=hashed_pw
    )

    # DB Ausführung
    await database.execute(query)
    return {"message": "Benutzer erfolgreich angelegt!"}

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
    
    # Token erzeugen
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTEN)
    access_token = create_access_token(
        data={"sub": found_user["email"]},
        expires_delta=access_token_expire
    )

    return {"access_token": access_token, "token_type": "bearer"}
