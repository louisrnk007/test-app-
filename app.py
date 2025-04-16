import streamlit as st
import openai
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="CoachBot - Assistant Sportif avec IA",
    page_icon="🤖",
    layout="centered"
)

# 🔍 Chargement des clients existants
if not os.path.exists("clients"):
    os.makedirs("clients")

clients = [f.replace(".json", "") for f in os.listdir("clients") if f.endswith(".json")]
st.sidebar.title("🤝 Bienvenue dans CoachBot")
client_select = st.sidebar.selectbox("Choisir un client", ["Nouveau client"] + clients)

# 📄 Formulaire client ou chargement
if client_select == "Nouveau client":
    st.sidebar.markdown("**📄 Créer un nouveau client**")
    nom = st.sidebar.text_input("Nom")
    prenom = st.sidebar.text_input("Prénom")
    objectif = st.sidebar.selectbox("Objectif", ["Perte de poids", "Prise de masse", "Remise en forme", "Autre"])
    niveau = st.sidebar.radio("Niveau", ["Débutant", "Intermédiaire", "Avancé"])

    if st.sidebar.button("Créer ce client"):
        client_id = f"{prenom.lower()}_{nom.lower()}"
        client_data = {
            "nom": nom,
            "prenom": prenom,
            "objectif": objectif,
            "niveau": niveau,
            "historique": []
        }
        with open(f"clients/{client_id}.json", "w") as f:
            json.dump(client_data, f, indent=2)
        st.success(f"Client {prenom} {nom} créé !")
        st.experimental_rerun()
else:
    client_id = client_select
    with open(f"clients/{client_id}.json") as f:
        client_data = json.load(f)
    st.sidebar.success(f"Client chargé : {client_data['prenom']} {client_data['nom']}")

# 🔍 Clé API et initialisation OpenAI
client_openai = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

st.title("🤖 CoachBot - Assistant Sportif avec IA")
st.write("Pose-moi une question sur l'entraînement ou la nutrition :")

question = st.text_input("💬 Ta question", placeholder="Ex : Quel est le meilleur déjeuner pour la muscu ?")

# 🧠 Fonction de réponse
def repondre_ia(prompt):
    completion = client_openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un coach sportif professionnel qui donne des conseils utiles, motivants et adaptés."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

# 🔄 Interaction et sauvegarde
if question:
    with st.spinner("CoachBot réfléchit..."):
        reponse = repondre_ia(question)
        st.success("CoachBot :")
        st.markdown(reponse)

        # 🔢 Enregistrement dans le fichier du client
        if client_select != "Nouveau client":
            client_data["historique"].append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "question": question,
                "reponse": reponse
            })
            with open(f"clients/{client_id}.json", "w") as f:
                json.dump(client_data, f, indent=2)

# 📜 Affichage historique
if client_select != "Nouveau client" and client_data["historique"]:
    with st.expander("📓 Historique des questions du client"):
        for item in reversed(client_data["historique"]):
            st.markdown(f"**🗓️ {item['date']}**")
            st.markdown(f"**Q :** {item['question']}")
            st.markdown(f"**A :** {item['reponse']}")
            st.markdown("---")


