# pages/user.py
import streamlit as st

def show():
    st.title("👤 Espace Utilisateur")
    st.write(f"Bienvenue {st.session_state.user} 👋")

    if st.button("Se déconnecter"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
