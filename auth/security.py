from passlib.context import CryptContext
from datetime import timedelta
from jose import jwt

# PW-Hash Kontext initialisieren
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# PW hashen
def hash_passwort(passwort: str):
    return pwd_context.hash(passwort)

# Token konfiguration
SECRET_KEY = "ramin ist der beste"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTEN = 30

# Access Token erstellen
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt