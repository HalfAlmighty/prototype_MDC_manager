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
                st.session_state.choice_radio = "Admin"  # Mise à jour radio
            else:
                st.session_state.page = "user"
                st.session_state.choice_radio = "User"   # Mise à jour radio
            st.success(f"Connexion réussie ! Bienvenue {username}")
            st.info("⚠️ Utilisez le menu de navigation pour accéder à votre page.")
        else:
            st.error("❌ Nom d'utilisateur vide.")

    if st.button("Créer un compte", key="login_register_btn"):
        st.session_state.page = "register"
        st.session_state.choice_radio = "Register"
        st.info("⚠️ Utilisez le menu de navigation pour accéder à la page d'inscription.")
