import streamlit as st
from openai import OpenAI

# 🔐 Sécurité de la clé API
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.title("🤖 CoachBot - Assistant Sportif avec IA")
st.write("Pose-moi une question sur l'entraînement ou la nutrition 👇")

message = st.text_input("Que veux-tu savoir ?")

def repondre_ia(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un coach sportif professionnel qui donne des conseils utiles, motivants et adaptés."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

if message:
    with st.spinner("CoachBot réfléchit..."):
        reponse = repondre_ia(message)
        st.success(reponse)
