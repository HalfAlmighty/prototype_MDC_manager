# views/login.py
import streamlit as st
from views import admin, user

ADMINS = ["j.riff", "g.saucy", "n.metz", "c.riemer", "m.ludwig"]

def show():
    st.title("🔐 Connexion")
    #Créer un formulaire
    with st.form("login_form"):
    username = st.text_input("Nom d'utilisateur", key="login_user")
    password = st.text_input("Mot de passe", type="password", key="login_pwd")

    # Bouton de soumission
    submitted = st.form_submit_button("Se connecter")
    
    if submitted:
        if username:
            st.session_state.user = username
            if username in ADMINS:
                st.session_state.page = "admin"
                st.rerun()
            else:
                st.session_state.page = "user"
            st.success(f"Connexion réussie ! Bienvenue {username}")
            st.rerun()
        else:
            st.error("❌ Nom d'utilisateur vide.")

    if st.button("Créer un compte", key="login_register_btn"):
        st.session_state.page = "register"
        st.rerun()



