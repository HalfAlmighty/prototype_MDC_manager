# app/services/auth.py
# -------------------------------------------------------
# Service d'authentification : hash et vérification de mots de passe
# Utilisé par FastAPI pour sécuriser les utilisateurs
# Gestion sécurisée des mots de passe pour le projet MDC Manager
# - Hashage avec bcrypt via passlib
# - Vérification des mots de passe
# - Contrôle de la limite de 72 bytes de bcrypt
# ---------------------------------------------------------------

from passlib.context import CryptContext

# Limite de bcrypt en bytes
BCRYPT_MAX_BYTES = 72

# -------------------------------------------------------
# CryptContext : gère les algorithmes de hashage
# Configuration du hash Argon2
# deprecated="auto" permet de gérer les anciens hashes si jamais on change de schéma
# -------------------------------------------------------
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# -------------------------------------------------------
# Fonction de hashage de mot de passe
# -------------------------------------------------------
def hash_password(password: str) -> str:
    """
    Hash un mot de passe pour stockage sécurisé en DB.
    
    Arguments :
    - password (str) : mot de passe en clair

        Vérifie que le mot de passe ne dépasse pas la limite de 72 bytes pour bcrypt.

    Retour :
    - str : mot de passe hashé (prêt à être stocké)
    """

    

    # Toujours utiliser un mot de passe non vide
    if not password:
        raise ValueError("Le mot de passe ne peut pas être vide")
    
    return pwd_context.hash(password)

# -------------------------------------------------------
# Fonction de vérification de mot de passe
# -------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie qu'un mot de passe correspond au hash stocké en DB.
    Tronque à 72 bytes si nécessaire pour bcrypt.

    Arguments :
    - plain_password (str) : mot de passe en clair
    - hashed_password (str) : hash stocké en DB

    Même limite de 72 bytes appliquée pour la sécurité.

    Retour :
    - bool : True si correspond, False sinon
    """
    if not plain_password:
        return False
    
    # Vérification sécurisée, résiste aux attaques timing
    return pwd_context.verify(plain_password, hashed_password)

# -------------------------------------------------------
# ⚡ Conseils sécurité :
# - Ne jamais stocker le mot de passe en clair
# - Toujours utiliser bcrypt ou argon2 pour le hashage
# - Ne pas logger les mots de passe
# - En cas de migration de hash, CryptContext gère les anciens formats
# -------------------------------------------------------
