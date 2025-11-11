# streamlit_chatbot.py
import streamlit as st
import requests
import json

# --- Configuration de la clé API ---
api_key = st.secrets["KIMI_API_KEY"]  # Mettre ta clé dans Secrets de Streamlit Cloud

# --- Initialisation du chat ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 Chatbot Kimi K2")

# --- Zone de saisie utilisateur ---
user_input = st.text_input("Votre message :", "")

if st.button("Envoyer") and user_input.strip() != "":
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Préparer la requête API avec tout l'historique
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "moonshotai/kimi-k2:free",
            "messages": st.session_state.chat_history,
            "provider": {"sort": "throughput"}
        })
    )

    # Récupérer la réponse du modèle
    if response.status_code == 200:
        result = response.json()
        reply = result['choices'][0]['message']['content']
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
    else:
        st.error(f"Erreur API : {response.status_code} - {response.text}")

# --- Affichage du chat historique ---
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**Vous** : {chat['content']}")
    else:
        st.markdown(f"**Kimi K2** : {chat['content']}")
