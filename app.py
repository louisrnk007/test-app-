import streamlit as st
import openai
from datetime import datetime

st.set_page_config(
    page_title="CoachBot - Assistant Sportif avec IA",
    page_icon="🏋️‍♂️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------- BARRE LATÉRALE ----------
st.sidebar.title("🧭 Menu")
st.sidebar.markdown("Bienvenue dans CoachBot !")

st.sidebar.markdown("---")
st.sidebar.markdown("📅 Date : " + datetime.now().strftime("%d/%m/%Y"))
st.sidebar.markdown("💬 Pose une question ci-dessous")
st.sidebar.markdown("💪 Programme")

# ---------- EN-TÊTE PRINCIPAL ----------
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🤖 CoachBot - Assistant Sportif avec IA</h1>", 
    unsafe_allow_html=True
)
st.markdown("<p style='text-align: center;'>Pose-moi une question sur l'entraînement ou la nutrition 👇</p>", unsafe_allow_html=True)

# ---------- INPUT UTILISATEUR ----------
question = st.text_input("💬 Que veux-tu savoir ?", placeholder="Ex : Comment prendre du muscle rapidement ?")

# ---------- FONCTION D’APPEL À OPENAI ----------
def repondre_ia(prompt):
    try:
        client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur : {e}"

# ---------- AFFICHAGE DE LA RÉPONSE ----------
if question:
    with st.spinner("CoachBot réfléchit... 🤔"):
        reponse = repondre_ia(question)

    st.markdown("### ✅ Réponse de CoachBot :")
    st.success(reponse)

