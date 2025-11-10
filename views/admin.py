# pages/admin.py
import streamlit as st
from webscraping import carloerba, vwr
from views import fournisseurs

def show():
    st.title("👑 Espace Administrateur")
    st.write(f"Connecté en tant que : **{st.session_state.user}**")
    st.markdown("---")
    st.title("🧪 Espace Admin - Webscraping")
    st.subheader(f"Connecté en tant que {st.session_state.get('user')}")

    fournisseurs.show()
    
    # Barre latérale (fixe) Choix du module de webscraping
    with st.sidebar:
        module_choice = st.radio(
        "Navigation",
        ["CarloErba", "VWR"],
        key="user_module_radio"
        )   

    st.markdown("---")
    
    # Affichage du module choisi
    if module_choice == "CarloErba":
        carloerba.show()
    elif module_choice == "VWR":
        vwr.show()

    st.divider()
    if st.button("Se déconnecter"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()



