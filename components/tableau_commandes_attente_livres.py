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

# ---------------------------------------------------------------
# 🧠 Chargement du fichier Excel
# ---------------------------------------------------------------
def load_excel_file(uploaded_file):
    """Charge le fichier Excel téléchargé par l’utilisateur."""
    try:
        df = pd.read_excel(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return None


# ---------------------------------------------------------------
# 🧮 Fonction principale : affichage du tableau interactif
# ---------------------------------------------------------------
def show_table():
    """Affiche un tableau filtrable des commandes à partir d’un fichier Excel."""

    st.subheader("📦 Tableau des commandes en attente ou livrées")

    # -----------------------------------------------------------
    # 1️⃣ Upload du fichier Excel
    # -----------------------------------------------------------
    st.markdown("### 📂 Import du fichier Excel")
    uploaded_file = st.file_uploader(
        "Importer un fichier Excel (.xlsx ou .xls)",
        type=["xlsx", "xls"]
    )

    # Si aucun fichier n'est encore chargé
    if uploaded_file is None and "df_commandes" not in st.session_state:
        st.info("Veuillez importer un fichier Excel pour continuer.")
        return

    # Si un fichier vient d’être uploadé, on le charge
    if uploaded_file is not None:
        df = load_excel_file(uploaded_file)
        if df is not None:
            st.session_state.df_commandes = df  # ✅ Sauvegarde en session
        else:
            return

    # Si aucun nouveau fichier mais des données déjà chargées
    df = st.session_state.get("df_commandes", None)
    if df is None:
        st.warning("Aucune donnée disponible.")
        return

    # -----------------------------------------------------------
    # 2️⃣ Zone de filtres dynamiques
    # -----------------------------------------------------------
    st.markdown("### 🔍 Filtres")
    filter_columns = [
        "Code article", "Référence", "Désignation", "Famille",
        "N°Fournisseur", "Fournisseur", "Preneur"
    ]

    filters = {}
    cols = st.columns(2)  # organisation des filtres sur deux colonnes

    for i, col in enumerate(filter_columns):
        with cols[i % 2]:
            options = df[col].dropna().unique()
            filters[col] = st.multiselect(
                f"Sélectionner {col}",
                options=options,
                default=None
            )

    # -----------------------------------------------------------
    # 3️⃣ Application des filtres
    # -----------------------------------------------------------
    filtered_df = df.copy()
    for col, selected_values in filters.items():
        if selected_values:
            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

    # -----------------------------------------------------------
    # 4️⃣ Affichage du tableau filtré
    # -----------------------------------------------------------
    if filtered_df.empty:
        st.warning("⚠️ Aucun résultat ne correspond aux filtres sélectionnés.")
        return

    st.markdown("---")
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

    # -----------------------------------------------------------
    # 5️⃣ Téléchargement des résultats filtrés
    # -----------------------------------------------------------

    # ✅ Génération du fichier Excel en mémoire
    output_excel = BytesIO()
    filtered_df.to_excel(output_excel, index=False, engine="openpyxl")
    output_excel.seek(0)

    # ✅ Génération du fichier CSV
    output_csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.markdown("### 💾 Télécharger les résultats filtrés")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Télécharger en Excel",
            data=output_excel,
            file_name="commandes_filtrees.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel"
        )
    with col2:
        st.download_button(
            label="📄 Télécharger en CSV",
            data=output_csv,
            file_name="commandes_filtrees.csv",
            mime="text/csv",
            key="download_csv"
        )

    st.success("✅ Tableau prêt à être téléchargé !")
