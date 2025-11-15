# backend/app/models/user.py

# pydantic est la librairie utilisée par FastAPI pour définir des "models" de données
# Ces models servent à :
#  - valider automatiquement les données reçues (types, format, champs requis)
#  - documenter automatiquement l'API (Swagger / OpenAPI)
from pydantic import BaseModel, EmailStr

# Définition d'un modèle Pydantic pour la requête de login.
# Ce modèle décrit exactement ce que le client doit envoyer dans le corps de la requête.
class UserLogin(BaseModel):
    # EmailStr est un type spécial qui valide que la chaîne est un e-mail valide.
    # Si la valeur envoyée n'est pas un e-mail, FastAPI renverra automatiquement
    # une erreur 422 (Unprocessable Entity) avant même d'entrer dans notre route.
    email: EmailStr

    # password est simplement une chaîne de caractères.
    # On ne met pas ici de règle complexe (longueur, caractères spéciaux) — on peut
    # ajouter ces validations plus tard si besoin.
    password: str

    # Remarque : ne JAMAIS stocker de mots de passe en clair dans la BDD.
    # Ici c'est juste le format attendu côté API. L'authentification réelle
    # nécessitera hashing (bcrypt/argon2) et vérification côté serveur.
