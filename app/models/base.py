# app/db/base.py
# ------------------------------------------------
# Définition du Base SQLAlchemy pour centraliser metadata
# ------------------------------------------------
from sqlalchemy.orm import declarative_base

# Base à importer dans alembic/env.py pour target_metadata
Base = declarative_base()
