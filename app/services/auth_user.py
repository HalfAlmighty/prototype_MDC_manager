from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.jwt import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Récupère l'utilisateur connecté via son token JWT.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Token invalide")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return user
