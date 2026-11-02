import pandas as pd
import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Pagina-instellingen
st.set_page_config(page_title="Liga Pro Gunfactor Checker V1", page_icon="🏓", layout="wide")

st.title("🏓 Liga Pro Gunfactor Checker V1")
st.subheader("Matchups, Statistieken & Gunfactors")

SHEET_ID = "1GJ3dpsw2ha2_FZKyS4rHnp-4-jVBxtkdu9AaWvnFUf4"

# 1. VERBINDING MAKEN VIA GSPREAD (Met de Secrets die je net hebt ingevuld)
@st.cache_resource
def get_gspread_client():
    scope = ["https://google.com", "https://googleapis.com"]
    creds_dict = dict(st.secrets["gspread"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    return gspread.authorize(creds)

try:
    client = get_gspread_client()
    sheet = client.open_by_key(SHEET_ID)
    
    # Open de tabbladen direct via gspread
    worksheet_db = sheet.get_worksheet(0)       # Eerste tabblad (tafeltennis_db)
    worksheet_poule = sheet.get_worksheet(1)    # Tweede tabblad (poule_historie)
    
    # Laad de pure data in (dit omzeilt de HTML-blokkade volledig!)
    data_db = worksheet_db.get_all_records()
    data_poule = worksheet_poule.get_all_records()
    
    # Omzetten naar dataframes voor weergave
    df_db = pd.DataFrame(data_db) if data_db else pd.DataFrame(columns=["SpelerA", "SpelerB", "Uitslag", "Gunfactor"])
    df_poule = pd.DataFrame(data_poule) if data_poule else pd.DataFrame(columns=["Poule", "Datum", "Winnaar"])
    
    st.success("Database succesvol LIVE gekoppeld via gspread! ✅")
except Exception as e:
    st.error(f"Verbindingsfout: {e}")
    st.info("Controleer of de gspread secrets goed zijn opgeslagen in Streamlit en of het client_email is toegevoegd aan de Google Sheet (Delen).")
    df_db, df_poule = pd.DataFrame(), pd.DataFrame()

# 2. TOON DATA IN DE APP
st.markdown("### 📊 Actuele Tafeltennis DB")
st.dataframe(df_db, use_container_width=True)

st.markdown("### 📜 Poule Historie")
st.dataframe(df_poule, use_container_width=True)

st.divider()

# 3. INTERACTIE SECTIE (Schrijft nu direct live terug naar de sheet!)
st.markdown("### 🛠️ Acties")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Uitslag registreren")
    speler_a = st.text_input("Speler A", key="sa")
    speler_b = st.text_input("Speler B", key="sb")
    uitslag = st.text_input("Uitslag (bijv. 3-1)", key="uits")
    gunfactor = st.text_input("Gunfactor score", key="gun")
    
    if st.button("Uitslag Toevoegen", type="primary"):
        if speler_a and speler_b:
            try:
                # Voeg een rij toe aan het eerste tabblad
                worksheet_db.append_row([speler_a, speler_b, uitslag, gunfactor])
                st.success("Uitslag automatisch toegevoegd aan Google Sheets!")
                st.rerun()
            except Exception as e:
                st.error(f"Fout bij opslaan: {e}")
        else:
            st.error("Vul tenminste Speler A en Speler B in.")

with col2:
    st.markdown("#### Poule afronden")
    poule_naam = st.text_input("Poule Naam", key="pn")
    winnaar = st.text_input("Winnaar Poule", key="wp")
    
    if st.button("Poule Opslaan"):
        if poule_naam:
            try:
                datum_vandaag = datetime.now().strftime("%Y-%m-%d %H:%M")
                # Voeg een rij toe aan het tweede tabblad
                worksheet_poule.append_row([poule_naam, datum_vandaag, winnaar])
                st.success("Poule automatisch opgeslagen in Google Sheets!")
                st.rerun()
            except Exception as e:
                st.error(f"Fout bij opslaan poule: {e}")
        else:
            st.error("Vul een poulenaam in.")
