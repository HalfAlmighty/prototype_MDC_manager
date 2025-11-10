# webscraping/carloerba.py

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO

def show():
    st.header("🔍 Scraping Carlo Erba")

    # -------------------------------
    # 1️⃣ Connexion Carlo Erba
    # -------------------------------
    st.subheader("🔐 Connexion Carlo Erba")

    email = st.text_input("Email professionnel")
    password = st.text_input("Mot de passe", type="password")

    # -------------------------------
    # 2️⃣ Choix des références
    # -------------------------------
    st.subheader("📦 Sélection des références à analyser")

    search_option = st.radio(
        "Méthode de sélection :",
        ["Excel", "Manuel", "Excel + Manuel"],
        horizontal=True
    )

    excel_file = None
    if search_option in ["Excel", "Excel + Manuel"]:
        excel_file = st.file_uploader("Importer un fichier Excel (.xlsx ou .xls)", type=["xlsx", "xls"])

    manual_references = st.text_input("Références manuelles (séparées par une virgule)")

    # -------------------------------
    # 3️⃣ Lancer le scraping
    # -------------------------------
    if st.button("🚀 Lancer le scraping"):
        carloerba_scraper(email, password, excel_file, manual_references, search_option)

    # -------------------------------
    # 🧠 7️⃣ Affichage du dernier résultat s’il existe
    # -------------------------------
    if "df_carloerba" in st.session_state and st.session_state.df_carloerba is not None:
        df = st.session_state.df_carloerba

        def color_availability(val):
            if val == "En stock":
                return "background-color: #90EE90; color: black;"
            elif "Sous" in val:
                return "background-color: #FFD700; color: black;"
            else:
                return "background-color: #F08080; color: black;"

        st.dataframe(df.style.applymap(color_availability, subset=["Disponibilité"]))

        # ✅ Génération du fichier Excel en mémoire
        output = BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)

        # ✅ Bouton de téléchargement stable
        st.download_button(
            label="📥 Télécharger les résultats Excel",
            data=output,
            file_name="resultats_scraping_carloerba.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_excel"
        )


def carloerba_scraper(email, password, excel_file, manual_references, search_option):
    if not email or not password:
        st.warning("⚠️ Veuillez entrer vos identifiants.")
        return

    session = requests.Session()
    login_page_url = "https://www.carloerbareagents.com/cerstorefront/cer-fr/login"
    resp = session.get(login_page_url)
    soup = BeautifulSoup(resp.text, "lxml")
    token_field = soup.find("input", {"name": "CSRFToken"})

    if not token_field:
        st.error("Impossible d’obtenir le jeton CSRF — vérifie la connexion internet.")
        return

    csrf_token = token_field["value"]

    payload = {
        "j_username": email,
        "j_password": password,
        "CSRFToken": csrf_token
    }

    login_url = "https://www.carloerbareagents.com/cerstorefront/cer-fr/j_spring_security_check"
    response = session.post(login_url, data=payload, allow_redirects=False)

    if response.status_code != 302:
        st.error("❌ Connexion échouée — identifiants invalides ou site indisponible.")
        return

    st.success("✅ Connexion réussie !")

    # -------------------------------
    # 4️⃣ Lecture des références
    # -------------------------------
    references = []

    if search_option in ["Excel", "Excel + Manuel"] and excel_file:
        try:
            df_refs = pd.read_excel(excel_file)
            if "Référence" not in df_refs.columns:
                st.error("Le fichier Excel doit contenir une colonne nommée 'Référence'")
                return
            references.extend(df_refs["Référence"].dropna().astype(str).tolist())
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier Excel : {e}")
            return

    if search_option in ["Manuel", "Excel + Manuel"] and manual_references:
        references.extend([r.strip() for r in manual_references.split(",") if r.strip()])

    if not references:
        st.warning("⚠️ Aucune référence fournie.")
        return

    # -------------------------------
    # 5️⃣ Scraping Carlo Erba
    # -------------------------------
    st.info(f"🔍 Scraping de {len(references)} références...")
    progress = st.progress(0)
    results = []

    for i, ref in enumerate(references):
        url = f"https://www.carloerbareagents.com/cerstorefront/cer-fr/search/?text={ref}"
        try:
            r = session.get(url, timeout=15)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                products = soup.find_all("tr", class_="quickAddToCart")

                for product in products:
                    try:
                        name = product.find("input", {"name": "productNamePost"}).get("value")
                        price = product.find("input", {"name": "productPostPrice"}).get("value")
                        availability_icon = product.find("i")
                        avail = availability_icon.get("title") if availability_icon else "Non précisé"

                        if "stock" in avail.lower():
                            dispo = "En stock"
                        elif "15" in avail:
                            dispo = "Sous 15 jours"
                        elif "30" in avail:
                            dispo = "Sous 30 jours"
                        else:
                            dispo = "Non précisé"

                        results.append({
                            "Référence": ref,
                            "Produit": name,
                            "Prix (€)": price,
                            "Disponibilité": dispo
                        })
                    except Exception:
                        continue
        except Exception:
            continue

        progress.progress((i + 1) / len(references))

    if not results:
        st.warning("Aucun produit trouvé.")
        return

    df = pd.DataFrame(results)
    st.success("✅ Scraping terminé !")

    # ✅ Sauvegarde dans la session (permet d’éviter la disparition après téléchargement)
    st.session_state.df_carloerba = df
