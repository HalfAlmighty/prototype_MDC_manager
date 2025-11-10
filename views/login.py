# pages/login.py
import streamlit as st
from auth_db import verify_user

def show():
    st.title("🔐 Connexion Test")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        user = verify_user(username, password)

        if user:
            st.session_state.user = username
            if user["is_admin"]:
                st.session_state.page = "admin"
            else:
                st.session_state.page = "user"
            st.rerun()
        else:
            st.error("❌ Nom d'utilisateur vide.")
