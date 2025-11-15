# migrations/env.py
# -------------------------------------------------------
# Alembic environment pour gérer les migrations de DB
# -------------------------------------------------------

# Charger le fichier .env
from dotenv import load_dotenv
load_dotenv()  # va chercher le .env à la racine du projet

import sys
import os

# Ajouter la racine du projet au path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import Base et tous les modèles pour autogenerate
from app.models.base import Base
from app.models.user import User

# -------------------------------------------------------
# Configuration Alembic
# -------------------------------------------------------
# lit le fichier alembic.ini
config = context.config

# Setup logging
fileConfig(config.config_file_name)

# -------------------------------------------------------
# Connexion à la DB via variable d'environnement
# -------------------------------------------------------
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL non défini dans ton .env")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# target_metadata sert à autogenerate
target_metadata = Base.metadata

# -------------------------------------------------------
# Fonctions pour migration offline/online
# -------------------------------------------------------
def run_migrations_offline():
    """Run migrations without DB connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations avec DB connectée."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# -------------------------------------------------------
# Choix mode offline/online
# -------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
