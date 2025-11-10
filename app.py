# app.py
import streamlit as st
from auth_db import init_db
from components.clock import display_clock

# --- Initialisation ---
st.set_page_config(page_title="MDC Manager", layout="centered")
init_db()

st.sidebar.markdown("---")
st.sidebar.subheader("DEBUG")
st.sidebar.write("Page actuelle :", st.session_state.get("page"))
st.sidebar.write("Utilisateur :", st.session_state.get("user"))

# --- Import des views ---
from views import login, register, admin, user

# --- Initialisation de session_state ---
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None

# --- Barre latérale (fixe) ---
with st.sidebar:
    display_clock(color="white", size="30px", show_seconds=True)
    # Ajout d'un petit menu
    st.markdown("---")

# --- Routage ---
page = st.session_state.page

if page == "login":
    login.show()
elif page == "register":
    register.show()
elif page == "admin":
    admin.show()
elif page == "user":
    user.show()
else:
    st.error("Page inconnue.")














