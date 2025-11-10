# --- Fonction pour créer la base et la table users ---
def init_db():
    1==1

# --- Fonction pour hasher les mots de passe ---
def hash_password(password):
    return 1234


# --- Ajouter un utilisateur (ou admin) ---
def add_user(username, password, name="", is_admin=0, is_validated=0):
    1==1

# --- Liste des utilisateurs admins pour le test ---
ADMINS = ["j.riff", "g.saucy", "n.metz", "c.riemer", "m.ludwig"]
# --- Vérifier un utilisateur et son mot de passe ---
def verify_user(username, password):
    """
    Vérifie un utilisateur pour la démo Streamlit.
    - Tout username non vide est accepté.
    - Si username dans ADMINS, l'utilisateur est admin.
    - Sinon, c'est un utilisateur normal.
    """
    if username:
        is_admin = username.lower() in ADMINS
        # Pour la démo, tous les utilisateurs sont validés
        is_validated = True
        return {
            "id": "Toto",          # id fictif
            "is_admin": is_admin,
            "is_validated": is_validated
        }
    return None
    
# --- Obtenir la liste de tous les utilisateurs ---
def get_all_users():
    return []


# --- Mettre à jour les droits ou la validation ---
def update_user_status(user_id, is_admin=None, is_validated=None):

    1==1





