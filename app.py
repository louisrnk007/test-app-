import streamlit as st
import openai
import json
import os
import datetime
import requests

# --- Configuration ---
openai.api_key = st.secrets["openai"]["api_key"]
CLIENTS_FILE = "clients.json"

def charger_clients():
    if os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, "r") as f:
            return json.load(f)
    return {}

def sauvegarder_clients(clients):
    with open(CLIENTS_FILE, "w") as f:
        json.dump(clients, f, indent=2)

def envoyer_question(question):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erreur : {e}"

def afficher_salles_autour():
    # Cette fonction utilise IPinfo pour estimer la position et place des markers avec Leaflet
    try:
        ip = requests.get("https://api.ipify.org").text
        data = requests.get(f"https://ipinfo.io/{ip}/json").json()
        if "loc" in data:
            lat, lon = map(float, data["loc"].split(","))
            st.map(data=[{"lat": lat, "lon": lon}], zoom=12)
    except:
        st.warning("Impossible de localiser l'utilisateur.")

# --- Interface Streamlit ---
st.set_page_config(page_title="CoachBot", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 Assistant Sportif</h1>", unsafe_allow_html=True)

# Chargement des clients
clients = charger_clients()
client_id = None

# --- Barre latérale ---
st.sidebar.title("👋 Bienvenue")
st.sidebar.write("Gérer les clients")
choix = st.sidebar.selectbox("Choisir un client", ["Nouveau client"] + list(clients.keys()))

if choix == "Nouveau client":
    with st.sidebar.form("formulaire_client"):
        email = st.text_input("Email")
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        objectif = st.selectbox("Objectif", ["Remise en forme", "Prise de masse", "Perte de poids"])
        niveau = st.radio("Niveau", ["Débutant", "Intermédiaire", "Avancé"])
        submit = st.form_submit_button("Créer ce client")

    if submit and email and nom:
        client_id = email.lower()
        if client_id not in clients:
            clients[client_id] = {
                "nom": nom,
                "prenom": prenom,
                "email": email,
                "objectif": objectif,
                "niveau": niveau,
                "historique": []
            }
            sauvegarder_clients(clients)
          st.rerun()
        else:
            st.sidebar.warning("Ce client existe déjà.")
else:
    client_id = choix
    client = clients[client_id]
    st.sidebar.markdown(f"**{client['prenom']} {client['nom']}**")
    st.sidebar.markdown(f"Objectif : `{client['objectif']}` | Niveau : `{client['niveau']}`")

# --- Partie centrale ---
if client_id:
    st.markdown("<h4>Pose-moi une question sur l'entraînement ou la nutrition :</h4>", unsafe_allow_html=True)
    question = st.text_input("💬 Ta question", placeholder="Ex : Quel est le meilleur déjeuner pour la muscu ?")

    if question:
        reponse = envoyer_question(question)
        st.markdown(f"**CoachBot** : {reponse}")

        clients[client_id]["historique"].append({
            "date": datetime.datetime.now().isoformat(),
            "question": question,
            "reponse": reponse
        })
        sauvegarder_clients(clients)

    if st.checkbox("📜 Voir les anciennes questions"):
        for echange in reversed(clients[client_id]["historique"]):
            st.markdown(f"**{echange['date'].split('T')[0]}**")
            st.write(f"**Q:** {echange['question']}")
            st.write(f"**A:** {echange['reponse']}")
            st.markdown("---")

    if st.checkbox("📍 Salles de sport à proximité"):
        afficher_salles_autour()
else:
    st.info("Crée un client dans le menu latéral pour commencer.")


