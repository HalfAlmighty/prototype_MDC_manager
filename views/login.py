# views/login.py
import streamlit as st
from views import admin, user

ADMINS = ["j.riff", "g.saucy", "n.metz", "c.riemer", "m.ludwig"]

def show():
    st.title("🔐 Connexion")
    username = st.text_input("Nom d'utilisateur", key="login_user")
    password = st.text_input("Mot de passe", type="password", key="login_pwd")

    if st.button("Se connecter", key="login_btn"):
        if username:
            st.session_state.user = username
            if username in ADMINS:
                st.session_state.page = "admin"
            else:
                st.session_state.page = "user"
            st.success(f"Connexion réussie ! Bienvenue {username}")
        else:
            st.error("❌ Nom d'utilisateur vide.")

    if st.button("Créer un compte", key="login_register_btn"):
        st.session_state.page = "register"

