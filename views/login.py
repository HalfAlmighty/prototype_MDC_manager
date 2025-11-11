# views/login.py
import streamlit as st

# Liste des administrateurs
ADMINS = ["j.riff", "g.saucy", "n.metz", "c.riemer", "m.ludwig"]

def show():
    st.title("🔐 Connexion")

    # Formulaire de connexion
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur", key="login_user")
        password = st.text_input("Mot de passe", type="password", key="login_pwd")
        submitted = st.form_submit_button("Se connecter")

    if submitted:
        if not username:
            st.error("❌ Nom d'utilisateur vide.")
            return

        # Enregistrement du user dans la session
        st.session_state.user = username

        # Vérification du type d'utilisateur
        if username in ADMINS:
            st.session_state.page = "admin"
            st.success(f"👑 Connexion admin réussie ! Bienvenue {username}")
            st.rerun()

        elif username.lower() == "test":
            st.session_state.page = "test"
            st.success(f"🧪 Connexion test réussie ! Bienvenue {username}")
            st.rerun()
     
        elif username.lower() == "chatbot":
            st.session_state.page = "chatbot"
            st.success(f"🧪 Connexion test réussie ! Bienvenue {username}")
            st.rerun()

        else:
            st.session_state.page = "user"
            st.success(f"✅ Connexion réussie ! Bienvenue {username}")
            st.rerun()

    # Lien vers la création de compte
    if st.button("Créer un compte", key="login_register_btn"):
        st.session_state.page = "register"
        st.rerun()

