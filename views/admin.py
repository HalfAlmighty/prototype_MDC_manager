# pages/admin.py
import streamlit as st
from auth_db import get_all_users, update_user_status

def show():
    st.title("👑 Espace Administrateur")
    st.write(f"Connecté en tant que : **{st.session_state.user}**")

    from webscraping import carloerba

    st.markdown("---")
    st.title("🧪 Espace de scraping Carlo Erba")
    carloerba.show()

    users = get_all_users()
    for u in users:
        uid, uname, name, is_admin, is_validated, created = u
        st.markdown(
            f"**{uname}** ({name}) — Admin: {bool(is_admin)} — Validé: {bool(is_validated)} — Créé le {created}"
        )

        col1, col2 = st.columns(2)
        if col1.button(f"Valider {uname}", key=f"val_{uid}"):
            update_user_status(uid, is_validated=1)
            st.rerun()
        if col2.button(f"Donner droits admin à {uname}", key=f"adm_{uid}"):
            update_user_status(uid, is_admin=1)
            st.rerun()

    st.divider()
    if st.button("Se déconnecter"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
