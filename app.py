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
if "choice_radio" not in st.session_state:
    st.session_state.choice_radio = st.session_state.page

# --- Barre latérale (fixe) ---
with st.sidebar:
    display_clock(color="white", size="20px", show_seconds=True)
    # Ajout d'un petit menu
    st.markdown("---")
    # Radio avec valeur initiale = session_state.choice_radio
    choice = st.radio(
        "Navigation",
        ["Login", "Register", "Admin", "User"],
        index=["login", "register", "admin", "user"].index(st.session_state.choice_radio)
    )
    
    # Si l'utilisateur change le radio
    if choice.lower() != st.session_state.choice_radio:
        st.session_state.choice_radio = choice.lower()
        st.session_state.page = choice.lower()

st.sidebar.write("Navigation :", choice)


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











