# pages/register.py
import streamlit as st

def show():
    st.title("📝 Créer un compte")

    name = st.text_input("Nom complet")
    username = st.text_input("Nom d'utilisateur souhaité")
    password = st.text_input("Mot de passe", type="password")

    if st.button("S'inscrire"):
        st.success("✅ Compte créé ! En attente de validation par un administrateur.")
        st.session_state.page = "login"
        st.rerun()

    if st.button("Retour à la connexion"):
        st.session_state.page = "login"
        st.rerun()

