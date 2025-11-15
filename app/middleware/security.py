"""
---------------------------------------------------------------
security.py
---------------------------------------------------------------
Middlewares de sécurité pour FastAPI
- CORS strict
- Logs sécurité
- Rate-limit anti brute-force sur /auth/login
- Headers anti-XSS / anti-clickjacking
---------------------------------------------------------------
"""

# ===============================================================
# 1. CORS STRICT (Limiter les origines autorisées)
# ===============================================================
from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    """
    Configure les règles CORS de l'application.
    Par défaut, seules 2 origines peuvent appeler ton API :
    - ton futur front React (localhost:3000)
    - ton site déployé
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://tonsite.com"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["Authorization", "Content-Type"],
    )


# ===============================================================
# 2. LOGS DE SÉCURITÉ (Chaque requête est loggée)
# ===============================================================
import time
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware qui logge chaque requête
    utile pour suivre les accès suspects / attaques
    """
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = round(time.time() - start, 3)

        print(f"[SECURITY] {request.client.host} → {request.url.path} → {response.status_code} ({duration}s)")
        return response


# ===============================================================
# 3. RATE LIMIT (Bruteforce protection sur /auth/login)
# ===============================================================
from fastapi import HTTPException

login_attempts = {}

class RateLimitLoginMiddleware(BaseHTTPMiddleware):
    """
    Limite les tentatives de login à 5 par minute pour une IP.
    Évite les attaques par force brute.
    """
    async def dispatch(self, request, call_next):

        if request.url.path == "/auth/login":
            ip = request.client.host
            now = time.time()

            # garder seulement les tentatives des 60 dernières secondes
            attempts = login_attempts.get(ip, [])
            attempts = [t for t in attempts if now - t < 60]
            login_attempts[ip] = attempts

            if len(attempts) >= 5:
                raise HTTPException(429, "Trop de tentatives, réessaie dans 1 minute")

            attempts.append(now)
            login_attempts[ip] = attempts

        return await call_next(request)


# ===============================================================
# 4. SECURITY HEADERS (Anti-XSS, Anti-Clickjacking)
# ===============================================================
from fastapi import FastAPI

def setup_security_headers(app: FastAPI):
    """
    Ajoute des headers HTTP pour renforcer la sécurité :
    - XSS Protection
    - Interdiction d'ouvrir dans un iframe
    - Protection des MIME types
    """
    @app.middleware("http")
    async def add_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response
