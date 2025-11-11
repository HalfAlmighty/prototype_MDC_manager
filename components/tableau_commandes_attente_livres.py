# ===============================================================
# 📘 Module : tableau_commandes_attente_livres.py
# 📍 Chemin : components/tableau_commandes_attente_livres.py
# 🧩 Description :
# Ce module Streamlit permet d'importer, filtrer et afficher
# un tableau Excel de commandes. Il inclut :
#  - Upload de fichier Excel (compatible Streamlit Cloud)
#  - Filtres multi-colonnes interactifs
#  - Téléchargement du tableau filtré (Excel ou CSV)
#  - Conservation du tableau en session (stable après téléchargement)
# ===============================================================

import streamlit as st
import pandas as pd
from io import BytesIO

# -------------------------------------------------------------------------
# 🧩 Fonction principale d'affichage du tableau des commandes
# -------------------------------------------------------------------------
def show_table():
    st.title("📦 Consultation des commandes en attente ou livrées")

    # --- Étape 1 : Importation du fichier Excel ---
    st.subheader("1️⃣ Importer un fichier Excel")
    excel_file = st.file_uploader(
        "Importer un fichier Excel (.xlsx ou .xls)",
        type=["xlsx", "xls"]
    )

    if excel_file is None:
        st.info("Veuillez importer un fichier Excel pour continuer.")
        return

  # --- Étape 2 : Lecture sécurisée du fichier Excel ---
    try:
        # Lecture automatique selon l'extension
        if excel_file.name.endswith(".xlsx"):
            df = pd.read_excel(excel_file, engine="openpyxl")
        elif excel_file.name.endswith(".xls"):
            df = pd.read_excel(excel_file, engine="xlrd")
        else:
            st.error("Format non reconnu : veuillez importer un fichier .xlsx ou .xls.")
            return

    except ImportError as e:
        st.error(f"⚠️ Dépendance manquante : {e}")
        st.info("Installez-la dans requirements.txt : `openpyxl` et `xlrd>=2.0.1`.")
        return
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return

    # -------------------------------------------------------------------------
    # Étape 3 : Interface de filtrage
    # -------------------------------------------------------------------------
    st.subheader("2️⃣ Filtres interactifs")

    colonnes_filtrables = {
        "Code article": "A",
        "Référence": "B",
        "Désignation": "C",
        "Famille": "D",
        "N°Fournisseur": "G",
        "Fournisseur": "H",
        "Code acheteur": "N",
        "Preneur": "O",
    }

    # Sélection du filtre principal (détermine la hiérarchie)
    filtre_principal = st.radio(
        "🧭 Choisissez le filtre principal :",
        list(colonnes_filtrables.keys()),
        horizontal=True,
    )

    # Fonction de tri alphanumérique croissant
    def tri_alpha(values):
        return sorted(values.astype(str).unique(), key=lambda x: x.lower())

    # Boîtes déroulantes avec autocomplétion (multi-sélection)
    selections = {}
    for nom_col in colonnes_filtrables.keys():
        col_values = df[nom_col].dropna()
        col_values_sorted = tri_alpha(col_values)

        # Si ce n’est pas le filtre principal, on adapte selon les sélections précédentes
        if nom_col != filtre_principal:
            # On ne filtre que si une sélection principale existe
            principal_sel = selections.get(filtre_principal)
            if principal_sel:
                df_filtre = df[df[filtre_principal].isin(principal_sel)]
                col_values_sorted = tri_alpha(df_filtre[nom_col].dropna())

        selections[nom_col] = st.multiselect(
            f"{nom_col} :", 
            options=col_values_sorted,
            default=[],
            placeholder=f"Sélectionner un ou plusieurs {nom_col.lower()}..."
        )

    # -------------------------------------------------------------------------
    # Étape 4 : Application des filtres cumulés
    # -------------------------------------------------------------------------
    df_filtre = df.copy()
    for col, valeurs in selections.items():
        if valeurs:
            df_filtre = df_filtre[df_filtre[col].isin(valeurs)]

    # -------------------------------------------------------------------------
    # Étape 5 : Affichage du tableau filtré
    # -------------------------------------------------------------------------
    st.subheader("3️⃣ Résultats filtrés")

    if df_filtre.empty:
        st.warning("Aucun résultat trouvé pour les critères choisis.")
    else:
        st.dataframe(df_filtre, use_container_width=True)
        st.success(f"✅ {len(df_filtre)} lignes affichées.")

    # -------------------------------------------------------------------------
    # Étape 6 : Téléchargement du résultat
    # -------------------------------------------------------------------------
    st.subheader("4️⃣ Télécharger le tableau filtré")

    output = BytesIO()
    df_filtre.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    st.download_button(
        label="📥 Télécharger en Excel",
        data=output,
        file_name="commandes_filtrees.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_excel"
    )

    # Sauvegarde en session (persistance)
    st.session_state.df_commandes_filtrees = df_filtre
