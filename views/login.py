# pages/login.py
import streamlit as st
from auth_db import verify_user

def show():
    st.title("🔐 Connexion")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
                st.session_state.user = username
                st.session_state.page = "admin"
                st.rerun()
        else:
            st.error("❌ Identifiants incorrects.")

    if st.button("Créer un compte"):
        register.show()


