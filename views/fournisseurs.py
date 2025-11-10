# pages/fournisseurs.py
import streamlit as st
import pandas as pd
from webscraping import linde_france, roth_sochiel, ugap, para_medical_hygiene
from webscraping import carloerba, fisher_scientific, ver_labo2000, vwr, willy_leissner

def show():
    st.title("Comparateur Fournisseurs - Test Modules")

    # Exemple de données
    data = [
        {"famille": "BOUTEILLE DE GAZ QUALITE INDUSTRIEL", "fournisseur": "LINDE FRANCE", "lot": "GAZ CARBONIQUE SOLIDE"},
        {"famille": "CONSOMMABLE POUR LA BIOLOGIE", "fournisseur": "ROTH SOCHIEL", "lot": "Lot A"},
        {"famille": "CONSOMMABLE POUR LA BIOLOGIE", "fournisseur": "UGAP", "lot": "Lot B"},
        {"famille": "CONSOMMABLE POUR L'HYGIENE ET LA SECURITE - EPI", "fournisseur": "PARA MEDICAL HYGIENE", "lot": "Lot C"},
    ]
    df = pd.DataFrame(data)

    familles = df['famille'].unique()
    famille_selected = st.sidebar.selectbox("Choisir une famille", familles)

    fournisseurs_list = df[df['famille'] == famille_selected]['fournisseur'].unique()
    for fournisseur in fournisseurs_list:
        lots = df[(df['famille'] == famille_selected) & (df['fournisseur'] == fournisseur)]['lot'].tolist()
        with st.expander(fournisseur):
            if fournisseur == "LINDE FRANCE":
                linde_france.show(famille_selected, lots)
            elif fournisseur == "ROTH SOCHIEL":
                roth_sochiel.show(famille_selected, lots)
            elif fournisseur == "UGAP":
                ugap.show(famille_selected, lots)
            elif fournisseur == "PARA MEDICAL HYGIENE":
                para_medical_hygiene.show(famille_selected, lots)
