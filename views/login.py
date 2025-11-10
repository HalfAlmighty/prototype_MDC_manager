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
        if username in ADMINS:
            st.session_state.page = "admin"
            st.session_state.page_radio = "admin"  # <-- force le radio
        else:
            st.session_state.page = "user"
            st.session_state.page_radio = "user"   # <-- force le radio

    else:
        st.error("❌ Nom d'utilisateur vide.")

    # --- Bouton création de compte ---
    if st.button("Créer un compte", key="register_button"):
        st.session_state.page = "register"
        st.session_state.page_radio = "register"  # <-- force le radio



