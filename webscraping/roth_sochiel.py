# webscraping/roth_sochiel.py
import streamlit as st

def show(famille, lots):
    st.write(f"### Module de test pour ROTH SOCHIEL")
    st.write(f"Famille sélectionnée : {famille}")
    
    st.write("Liste des lots disponibles :")
    for lot in lots:
        st.write(f"- {lot}")
