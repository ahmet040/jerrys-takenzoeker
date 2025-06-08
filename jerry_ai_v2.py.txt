import streamlit as st
import pandas as pd
import openai
import requests

# OpenAI API-key instellen (wordt niet opgeslagen)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Google Sheet CSV-link
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1nCLIs4_CVXYWNBUUPC52jeDugyYUWThh_Pmuo-Yly9U/export?format=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_CSV_URL)
    return df

def query_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Je bent Jerry AI v2.0, een slimme takenzoeker voor Werk Ahmet. Zoek binnen personeelsdata de juiste persoon bij elke taakvraag."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

st.set_page_config(page_title="Jerry AI v2.0 – Werk Ahmet", page_icon="🤖")
st.title("🤖 Jerry AI v2.0 – Takenzoeker met GPT")

st.markdown("Typ je vraag zoals je het zou zeggen. Jerry AI zoekt de juiste verantwoordelijke voor je.")

vraag = st.text_input("Wat wil je weten?", placeholder="Bijv. Wie doet inspectie zone D?")

if vraag:
    df = load_data()
    preview = "\n".join([f"{row['Naam']} – {row['Taak']} – {row['Afdeling']}" for _, row in df.iterrows()])
    prompt = f"Dit is het personeelsoverzicht:\n{preview}\n\nWie past het best bij de volgende taakvraag: {vraag}"
    antwoord = query_gpt(prompt)
    st.success(antwoord)
