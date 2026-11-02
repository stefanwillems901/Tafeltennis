import pandas as pd
import streamlit as st

# Pagina-instellingen
st.set_page_config(page_title="Liga Pro Gunfactor Checker V1", page_icon="🏓", layout="wide")

st.title("🏓 Liga Pro Gunfactor Checker V1")
st.subheader("Matchups, Statistieken & Gunfactors")

# 1. DATA INLADEN (Stabiele CSV-methode)
URL_TAFELTENNIS_DB = "https://google.com"
URL_POULE_HISTORIE = "https://google.com"

try:
    # We laden de data in met een User-Agent om netwerkblokkades te voorkomen
    df_db = pd.read_csv(URL_TAFELTENNIS_DB, storage_options={"User-Agent": "Mozilla/5.0"})
    df_poule = pd.read_csv(URL_POULE_HISTORIE, storage_options={"User-Agent": "Mozilla/5.0"})
    st.success("Database succesvol geladen! ✅")
except Exception as e:
    st.error(f"Er gaat iets mis bij het ophalen van de data: {e}")
    st.info("Controleer of de Google Sheet nog openbaar op 'Iedereen met de link' staat.")
    df_db, df_poule = pd.DataFrame(), pd.DataFrame()

# 2. TOON DATA IN DE APP (Als het laden is gelukt)
if not df_db.empty:
    st.markdown("### 📊 Actuele Tafeltennis DB")
    st.dataframe(df_db, use_container_width=True)

if not df_poule.empty:
    st.markdown("### 📜 Poule Historie")
    st.dataframe(df_poule, use_container_width=True)

st.divider()

# 3. INTERACTIE SECTIE (Knoppen voorbereid voor de Form-koppeling)
st.markdown("### 🛠️ Acties")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Uitslag registreren")
    # Hier komen straks je invoervelden (bijv. speler selecties)
    if st.button("Uitslag Toevoegen", type="primary"):
        st.info("Deze knop wordt nu gekoppeld aan het Google Formulier om veilig te schrijven!")

with col2:
    st.markdown("#### Poule afronden")
    if st.button("Poule Opslaan"):
        st.info("Deze knop wordt nu gekoppeld aan het Google Formulier om veilig te schrijven!")

