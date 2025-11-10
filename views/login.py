# views/login.py
import streamlit as st

# Liste des utilisateurs admin pour le test
ADMINS = ["j.riff", "g.saucy", "n.metz", "c.riemer", "m.ludwig"]

def show():
    st.title("🔐 Connexion")

    # Inputs utilisateur avec clé unique pour éviter le StreamlitDuplicateElementId
    username = st.text_input("Nom d'utilisateur", key="login_username")
    password = st.text_input("Mot de passe", type="password", key="login_password")

    # Bouton de connexion
    if st.button("Se connecter", key="login_btn"):
        if username:
            st.session_state.user = username

            # On met à jour page et radio menu
            if username in ADMINS:
                st.session_state.page = "admin"
                st.session_state.page_radio = "admin"
            else:
                st.session_state.page = "user"
                st.session_state.page_radio = "user"

            st.success(f"Connexion réussie ! Bienvenue {username}")
            st.info("⚠️ Utilisez le menu de navigation pour accéder à votre page.")
        else:
            st.error("❌ Nom d'utilisateur vide.")

    # Bouton création de compte
    if st.button("Créer un compte", key="login_register_btn"):
        st.session_state.page = "register"
        st.session_state.page_radio = "register"
        st.info("⚠️ Utilisez le menu de navigation pour accéder à la page d'inscription.")
