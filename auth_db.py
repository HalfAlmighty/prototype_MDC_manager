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
    Login test pour Streamlit Community :
    - Admins listés : j.riff, g.saucy, n.metz, c.riemer, m.ludwig
    - Tous les autres -> user
    - Mot de passe ignoré
    """
    if username:
        admins = ["j.riff", "g.saucy", "n.metz", "c.riemer", "m.ludwig"]
        is_admin = username.lower() in admins
        user_id = username  # on renvoie le nom saisi
        is_validated = True  # toujours validé pour le test

        return {
            "id": user_id,
            "is_admin": bool(is_admin),
            "is_validated": bool(is_validated)
        }

    return None
    
# --- Obtenir la liste de tous les utilisateurs ---
def get_all_users():
    return []


# --- Mettre à jour les droits ou la validation ---
def update_user_status(user_id, is_admin=None, is_validated=None):

    1==1


