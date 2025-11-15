# app/services/jwt.py

import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Variables d'environnement
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", 30))

# --------------------------------------
# Création des tokens
# --------------------------------------
def create_access_token(data: dict):
    """
    Crée un JWT d'accès avec expiration courte.
    """
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = data.copy()
    payload.update({"exp": expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    """
    Crée un JWT de refresh avec expiration longue.
    """
    expires = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = data.copy()
    payload.update({"exp": expires, "type": "refresh"})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# --------------------------------------
# Décodage des tokens
# --------------------------------------
def decode_access_token(token: str):
    """
    Décode un JWT d'accès.
    Retourne le payload si valide, sinon None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def decode_refresh_token(token: str) -> dict | None:
    """
    Décode un JWT de refresh.
    Retourne le payload si valide et de type 'refresh', sinon None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None
