# ---------------------------------------------------------------
# app/main.py
# ---------------------------------------------------------------
# C’est le "point d’entrée" de ton API FastAPI.
# On importe l'application FastAPI
# et on attache toutes les routes.
# ---------------------------------------------------------------

from fastapi import FastAPI
from app.api.routes import router

# On crée l'application FastAPI
app = FastAPI(
    title="MDC Manager API",
    description="Backend prototype du MDC Manager",
    version="0.1.0"
)

# On "monte" les routes dans l'application
# => Toutes les routes définies dans routes.py deviennent accessibles.
app.include_router(router)
