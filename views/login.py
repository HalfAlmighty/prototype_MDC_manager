# views/login.py
import streamlit as st
from auth_db import verify_user

# Liste des admins test
ADMINS = ["j.riff", "g.saucy", "n.metz", "c.riemer", "m.ludwig"]

def show():
    st.title("🔐 Connexion")

    # --- Champs de connexion avec clés uniques ---
    username = st.text_input("Nom d'utilisateur", key="login_username")
    password = st.text_input("Mot de passe", type="password", key="login_password")

    # --- Bouton connexion ---
    if st.button("Se connecter", key="login_button"):
        if username:
            # Vérification test (toujours accepte n'importe quel mot de passe)
            is_admin = username.lower() in ADMINS
            user = {"id": username, "is_admin": is_admin, "is_validated": True}

            # Mise à jour de la session
            st.session_state.user = username
            st.session_state.page = "admin" if is_admin
            st.session_state.page_radio = "admin"  # <-- force le radio
            else "user"
            
            # On laisse le routage de app.py gérer l'affichage
            st.session_state.page_radio = "user"  # <-- force le radio
        else:
            st.error("❌ Nom d'utilisateur vide.")

    # --- Bouton création de compte ---
    if st.button("Créer un compte", key="register_button"):
        st.session_state.page = "register"
        st.session_state.page_radio = "register"  # <-- force le radio


