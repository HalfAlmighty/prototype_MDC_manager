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
            # redirection admin ou user selon le nom
            st.session_state.user = username
            st.session_state.page = "admin" if user["is_admin"] else "user"
            st.rerun()
        else:
            st.error("❌ Nom d'utilisateur vide.")

    if st.button("Créer un compte"):
        st.session_state.page = "register"
        st.rerun()
