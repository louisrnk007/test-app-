import streamlit as st
from openai import OpenAI
import os

# Clé API via secrets
api_key = st.secrets["openai"]["api_key"]

# Création du client OpenAI
client = OpenAI(api_key=api_key)

# App UI
st.title("🤖 CoachBot - Assistant Sportif avec IA")
st.write("Pose-moi une question sur l'entraînement ou la nutrition 👇")

message = st.text_input("Que veux-tu savoir ?")

def repondre_ia(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un coach sportif professionnel."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Affichage
if message:
    try:
        reponse = repondre_ia(message)
        st.write("**CoachBot** :", reponse)
    except Exception as e:
        st.error(f"Erreur : {e}")
