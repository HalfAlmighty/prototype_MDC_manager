# app/routers/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db  # fonction qui retourne session SQLAlchemy
from app.models.user import User
from app.services.auth import hash_password, verify_password
from app.services.auth_user import get_current_user
from app.services.roles import require_admin
from app.services.jwt import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token  # <- il faut créer cette fonction
)
from pydantic import BaseModel

router = APIRouter()

# --------------------------------------
# Schemas Pydantic pour requêtes / responses
# --------------------------------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenWithRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# --------------------------------------
# Endpoint signup (création utilisateur)
# --------------------------------------
@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouvel utilisateur.
    Vérifie d'abord si le username ou l'email existe déjà.
    Ensuite, hache le mot de passe.
    """
    # Vérifier si l'utilisateur existe déjà
    db_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")

    # Hacher le mot de passe
    try:
        hashed_pw = hash_password(user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Création du nouvel utilisateur
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        role="user"  # par défaut
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Générer un token JWT
    access_token = create_access_token({"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --------------------------------------
# Endpoint login
# --------------------------------------
@router.post("/login", response_model=TokenWithRefresh)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Connecte un utilisateur existant.
    Vérifie l'existence du username et la correspondance du mot de passe.
    Retourne un token JWT si succès.
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Identifiant incorrect")

    # Vérifier le mot de passe
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")
    
    # Générer un token JWT
    access_token = create_access_token({"sub": db_user.username})
    refresh_token = create_refresh_token({"sub": db_user.username})  # <- ajouté

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # <- ajouté
        "token_type": "bearer"
    }


# --------------------------------------
# Endpoint refresh token
# --------------------------------------
class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    try:
        payload = decode_refresh_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token invalide")
        username = payload.get("sub")
        new_access = create_access_token({"sub": username})
        return {"access_token": new_access, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token expiré ou invalide")

# --------------------------------------
# Endpoint utilisateur connecté
# --------------------------------------
@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Retourne les informations de l'utilisateur connecté.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }

# --------------------------------------
# Endpoint admin uniquement
# --------------------------------------
@router.get("/admin/secret")
def admin_only(user = Depends(require_admin)):
    """
    Endpoint accessible uniquement aux admins.
    """
    return {"message": "Bienvenue maître Guillaume admin suprême 😎"}
