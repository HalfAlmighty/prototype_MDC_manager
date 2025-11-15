# ---------------------------------------------------------------
# app/api/routes.py
# ---------------------------------------------------------------
# Ce fichier regroupe les différents endpoints (routes HTTP)
# de ton API FastAPI.
# Chaque "router" correspond à un module (auth, users, data, etc.)
# ---------------------------------------------------------------

from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    """
    Endpoint test simple.
    Renvoie juste un message pour vérifier que le serveur fonctionne.
    """
    return {"message": "pong"}
