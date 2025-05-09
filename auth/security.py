from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv

load_dotenv()

# Token Header Prüfung
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Funktion, die den aktuellen Benutzer ermittelt und validiert
def get_current_user(token: str = Depends(oauth2_scheme)):

    # Fehlender oder falscher Token
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nicht autorisiert", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print("JWT Payload:", payload)

        user_mail: str = payload.get("sub")
        user_role: str = payload.get("role")

        if not user_mail or not user_role:
            raise credentials_exception
        
        return {"email": user_mail, "role": user_role}
    
    except JWTError:
        raise credentials_exception


# PW-Hash Kontext initialisieren
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# PW hashen
def hash_passwort(passwort: str):
    return pwd_context.hash(passwort)

# Token konfiguration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTEN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTEN", 30))

# Access Token erstellen
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTEN)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt