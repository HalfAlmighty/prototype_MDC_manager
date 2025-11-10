# app.py
import streamlit as st
from auth_db import init_db
from components.clock import display_clock

# --- Initialisation ---
st.set_page_config(page_title="MDC Manager", layout="centered")
init_db()

# --- Import des views ---
from views_custom import login, register, admin, user

# --- Barre latérale (fixe) ---
with st.sidebar:
    display_clock(color="white", size="20px", show_seconds=True)
    # Ajout d'un petit menu
    st.markdown("---")
    choice = st.radio("Navigation", ["Login", "Register", "Admin", "User"])
    st.session_state.page = choice.lower()
    

# --- Gestion de la session ---
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None

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
