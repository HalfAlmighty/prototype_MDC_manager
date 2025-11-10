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

    fournisseur = df['fournisseur'].unique()
    fournisseur_selected = st.sidebar.selectbox("Choisir un fournisseur", fournisseur)

    familles_list = df[df['fournisseur'] == fournisseur_selected]['famille'].unique()
    for famille in familles_list:
        lots = df[(df['fournisseur'] == fournisseur_selected) & (df['famille'] == famille)]['lot'].tolist()
        with st.expander(famille):
            if famille == "BOUTEILLE DE GAZ QUALITE INDUSTRIEL":
                linde_france.show(fournisseur_selected, lots)
            elif famille == "CONSOMMABLE POUR LA BIOLOGIE" & lots == "Lot A":
                roth_sochiel.show(fournisseur_selected, lots)
            elif famille == "CONSOMMABLE POUR LA BIOLOGIE" & lots == "Lot B":
                ugap.show(fournisseur_selected, lots)
            elif famille == "CONSOMMABLE POUR L'HYGIENE ET LA SECURITE - EPI":
                para_medical_hygiene.show(fournisseur_selected, lots)



