# --- Fonction pour créer la base et la table users ---
def init_db():
    1==1

# --- Fonction pour hasher les mots de passe ---
def hash_password(password):
    return 1234


# --- Ajouter un utilisateur (ou admin) ---
def add_user(username, password, name="", is_admin=0, is_validated=0):
    1==1

# --- Vérifier un utilisateur et son mot de passe ---
def verify_user(username, password):
    """
    Login test :
    - Pour certains noms, renvoie admin
    - Pour tous les autres, renvoie user
    """
    if not username:
        return None

    # Liste des admins
    admins = ["j.riff", "g.saucy", "n.metz", "c.riemer", "m.ludwig"]

    is_admin = username.lower() in admins

    return {
        "id": username,
        "is_admin": is_admin,
        "is_validated": True  # Toujours validé
    }

# --- Obtenir la liste de tous les utilisateurs ---
def get_all_users():
    return []


# --- Mettre à jour les droits ou la validation ---
def update_user_status(user_id, is_admin=None, is_validated=None):

    1==1
