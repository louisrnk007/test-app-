import streamlit as st
import json
import os
import folium
from streamlit_folium import st_folium

# Fichier pour stocker les clients
CLIENTS_FILE = "clients.json"

# Initialisation
if not os.path.exists(CLIENTS_FILE):
    with open(CLIENTS_FILE, "w") as f:
        json.dump({}, f)

# Chargement des données
def charger_clients():
    with open(CLIENTS_FILE, "r") as f:
        return json.load(f)

def sauvegarder_clients(clients):
    with open(CLIENTS_FILE, "w") as f:
        json.dump(clients, f, indent=2)

clients = charger_clients()

# Interface Streamlit
st.set_page_config(page_title="CoachBot", layout="wide")

# Sidebar - Gestion des clients
st.sidebar.title("👋 Bienvenue dans CoachBot")
st.sidebar.subheader("Gérer les clients")

email_selection = st.sidebar.selectbox("Choisir un client", ["Nouveau client"] + list(clients.keys()))

if email_selection == "Nouveau client":
    st.sidebar.subheader("📄 Créer un nouveau client")
    email = st.sidebar.text_input("E-mail")
    nom = st.sidebar.text_input("Nom")
    prenom = st.sidebar.text_input("Prénom")
    objectif = st.sidebar.selectbox("Objectif", ["Remise en forme", "Prise de masse", "Perte de poids", "Sport santé"])
    niveau = st.sidebar.radio("Niveau", ["Débutant", "Intermédiaire", "Avancé"])
    
    if st.sidebar.button("Créer ce client"):
        if email and nom and prenom:
            clients[email] = {
                "nom": nom,
                "prenom": prenom,
                "objectif": objectif,
                "niveau": niveau,
                "historique": []
            }
            sauvegarder_clients(clients)
            st.success(f"Client {prenom} {nom} créé !")
            st.rerun()
        else:
            st.sidebar.warning("Merci de remplir tous les champs.")
else:
    client = clients[email_selection]
    st.markdown(f"<h1 style='text-align:center;'>🤖 Assistant Sportif avec IA</h1>", unsafe_allow_html=True)
    
    st.subheader("Pose-moi une question sur l'entraînement ou la nutrition :")
    question = st.text_input("💬 Ta question", placeholder="Ex : Quel est le meilleur déjeuner pour la muscu ?")

    if question:
        # Simule une réponse IA ici (tu peux l'adapter à ton back OpenAI)
        reponse = f"Tu m'as demandé : {question} → Voici une réponse personnalisée basée sur ton profil ({client['objectif']}, niveau {client['niveau']})."

        # Affichage
        st.markdown(f"**CoachBot** : {reponse}")

        # Historique
        client["historique"].append({"question": question, "reponse": reponse})
        sauvegarder_clients(clients)

    # Affichage historique
    if client["historique"]:
        st.subheader("📜 Historique de tes questions :")
        for item in reversed(client["historique"][-5:]):
            st.markdown(f"- **Q** : {item['question']}\n- **A** : {item['reponse']}")

    # Affichage d'une carte avec les salles de sport à proximité
    st.subheader("📍 Salles de sport proches")
    m = folium.Map(location=[50.633, 5.567], zoom_start=13)  # tu peux changer les coords
    folium.Marker(location=[50.633, 5.567], popup="Basic-Fit").add_to(m)
    folium.Marker(location=[50.629, 5.570], popup="Jims Fitness").add_to(m)
    st_folium(m, width=700, height=400)
