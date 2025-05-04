from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2AuthorizationCodeBearer
import os
from dotenv import load_dotenv

# Env variables laden
load_dotenv()

# Env setzen
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTEN = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTEN")

# PW Hashconfig
pw_hashing = CryptContext(schemes=["bcrypt"], deprecated="auto")

# PW hashen
def pw_hash(password: str):
    return pw_hashing.hash(password)

# Access Token erstellen

def acces_token(data: dict, expire_time: timedelta = None):
    daten = data.copy()

    if expire_time:
        expire = datetime.utcnow() + expire_time
    else:
        expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE_MINUTEN

    daten.update({"exp": expire})

    token = jwt.encode(daten, SECRET_KEY, algorithm=ALGORITHM)

    return token

# Tokenprüfung config
oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="login")

# Tokenprüfung durchführen
def check_token(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nicht autorisierter Zugriff", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.encode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_mail: str = payload.get("sub")

        if user_mail is None:
            raise credentials_exception
        
        return user_mail
    
    except JWTError:
        raise credentials_exception
    

