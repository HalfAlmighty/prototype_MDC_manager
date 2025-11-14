# backend/app/core/config.py
from dotenv import load_dotenv
import os

# Charger le .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
