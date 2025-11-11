# ===============================================================
# 📘 Module : tableau_commandes_attente_livres.py
# 📍 Chemin : components/tableau_commandes_attente_livres.py
# 🧩 Description :
# Ce module Streamlit permet d'importer, filtrer et afficher
# un tableau Excel de commandes. Il inclut :
#  - Upload de fichier Excel (compatible Streamlit Cloud)
#  - Filtres hiérarchiques dynamiques (filtre principal)
#  - Téléchargement du tableau filtré (Excel)
#  - Conservation du tableau en session
# ===============================================================

import streamlit as st
import pandas as pd
from io import BytesIO


# -------------------------------------------------------------------------
# 🧩 Fonction principale
# -------------------------------------------------------------------------
def show_table():
    st.title("📦 Consultation des commandes en attente ou livrées")

    # === Étape 1 : Importation du fichier Excel ===
    st.subheader("1️⃣ Importer un fichier Excel")
    excel_file = st.file_uploader(
        "Importer un fichier Excel (.xlsx ou .xls)",
        type=["xlsx", "xls"]
    )

    if excel_file is None:
        st.info("Veuillez importer un fichier Excel pour continuer.")
        return

    # === Étape 2 : Lecture sécurisée du fichier Excel ===
    try:
        if excel_file.name.endswith(".xlsx"):
            df = pd.read_excel(excel_file, engine="openpyxl")
        elif excel_file.name.endswith(".xls"):
            df = pd.read_excel(excel_file, engine="xlrd")
        else:
            st.error("Format non reconnu : veuillez importer un fichier .xlsx ou .xls.")
            return
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return

    # --- Vérifie la présence minimale des colonnes nécessaires ---
    colonnes_attendues = [
        "Code article", "Référence", "Désignation", "Famille", "Date de la commande",
        "N° de commande", "N°Fournisseur", "Fournisseur", "Quantité", "PUHT", "Montant",
        "N° de confirmation", "Commentaire ligne", "Code acheteur", "Preneur"
    ]

    if not all(col in df.columns for col in colonnes_attendues):
        st.error("⚠️ Le fichier ne contient pas toutes les colonnes attendues. Vérifiez le format.")
        st.write("Colonnes attendues :", colonnes_attendues)
        st.write("Colonnes trouvées :", df.columns.tolist())
        return

    # === Étape 3 : Interface de filtrage hiérarchique ===
    st.subheader("2️⃣ Filtres interactifs avec hiérarchie")

    colonnes_filtrables = [
        "Code article", "Référence", "Désignation", "Famille",
        "N°Fournisseur", "Fournisseur", "Code acheteur", "Preneur"
    ]

    # --- Sélection du filtre principal ---
    filtre_principal = st.radio(
        "🧭 Choisissez le filtre principal :",
        colonnes_filtrables,
        horizontal=True,
    )

    # --- Fonction utilitaire de tri alpha ---
    def tri_alpha(values):
        return sorted(values.astype(str).unique(), key=lambda x: x.lower())

    # --- Sélection des valeurs du filtre principal ---
    valeurs_principales = tri_alpha(df[filtre_principal].dropna())
    selection_principale = st.multiselect(
        f"{filtre_principal} (filtre principal) :",
        options=valeurs_principales,
        placeholder=f"Sélectionnez un ou plusieurs {filtre_principal.lower()}...",
    )

    # --- Filtrage du DataFrame selon le filtre principal ---
    if selection_principale:
        df_filtre_base = df[df[filtre_principal].isin(selection_principale)]
    else:
        df_filtre_base = df.copy()

    # --- Création des autres filtres dépendants ---
    st.markdown("### 🔍 Filtres secondaires (affinage)")
    selections = {}

    for col in colonnes_filtrables:
        if col == filtre_principal:
            continue  # On ignore le filtre principal ici

        # Liste des valeurs disponibles après filtrage principal
        valeurs_possibles = tri_alpha(df_filtre_base[col].dropna())
        selections[col] = st.multiselect(
            f"{col} :", 
            options=valeurs_possibles,
            placeholder=f"Sélectionnez un ou plusieurs {col.lower()}..."
        )

    # --- Application des filtres cumulés ---
    df_filtre = df_filtre_base.copy()
    for col, valeurs in selections.items():
        if valeurs:
            df_filtre = df_filtre[df_filtre[col].isin(valeurs)]

    # === Étape 4 : Affichage du tableau ===
    st.subheader("3️⃣ Résultats filtrés")
    if df_filtre.empty:
        st.warning("Aucun résultat trouvé pour les critères choisis.")
    else:
        st.dataframe(df_filtre, use_container_width=True)
        st.success(f"✅ {len(df_filtre)} lignes affichées.")

    # === Étape 5 : Téléchargement du tableau filtré ===
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

    # Sauvegarde du tableau filtré en session
    st.session_state.df_commandes_filtrees = df_filtre

    st.markdown("---")

    st.divider()
    if st.button("Se déconnecter"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()

