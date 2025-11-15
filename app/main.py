# ---------------------------------------------------------------
# app/main.py
# ---------------------------------------------------------------
# Point d’entrée de l'API FastAPI.
# - Création de l'application
# - Définition de la route racine
# - Inclusion des routes du module app.api.routes
# ---------------------------------------------------------------

from fastapi import FastAPI
from app.api.routes import router

# Création de l'application FastAPI
app = FastAPI(
    title="MDC Manager API",
    description="Backend prototype du MDC Manager",
    version="0.1.0"
)

# ---------------------------------------------------------------
# ROUTE RACINE "/"
# ---------------------------------------------------------------
# Permet de tester rapidement si l’API répond.
# Appelée via :
#   GET https://mdc-manager-backend.onrender.com/
# ---------------------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Backend MDC Manager is running"
    }

# ---------------------------------------------------------------
# INCLUSION DES ROUTES
# ---------------------------------------------------------------
# On "monte" les routes définies dans routes.py
# Cela rend toutes les routes disponibles dans l'application.
# ---------------------------------------------------------------
app.include_router(router)
