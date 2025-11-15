# app/models/user.py (exemple minimal, commenté)
from sqlalchemy import Column, Integer, String
from app.models.base import Base  # ton Base existant dans app/models/base.py

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # "admin" ou "user"

