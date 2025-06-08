import streamlit as st
import pandas as pd

# Link naar je Google Sheet als CSV
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRj6zv1P__4vqaRkbLQAzGhT_eXGmWVRV54DAgwllvTg-4ZDCrs3MRwnE93MImTeMsfRzG7R1Nbh2Hl/pub?output=csv"

@st.cache_data
def load_data():
    df = pd.read_csv(SHEET_CSV_URL)
    return df

def zoek_persoon(vraag, df):
    vraag = vraag.lower()
    for i, row in df.iterrows():
        combined = ' '.join(str(val).lower() for val in row.values)
        if all(kw in combined for kw in vraag.split()):
            return row
    return None

st.title("🔍 Jerry's Takenzoeker – Werk Ahmet")
st.write("Typ hieronder je vraag. Jerry zoekt de juiste verantwoordelijke voor je.")

vraag = st.text_input("Wat wil je weten?", placeholder="Bijv. Wie doet de eindcontrole van laswerk?")

if vraag:
    df = load_data()
    resultaat = zoek_persoon(vraag, df)

    if resultaat is not None:
        st.success(f"**Verwijzing:** {resultaat['Naam']} – {resultaat['Taak']} ({resultaat['Afdeling']})")
    else:
        st.error("Geen match gevonden. Formuleer het anders of controleer de sheet.")
