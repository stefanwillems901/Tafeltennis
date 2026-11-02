import pandas as pd
import streamlit as st

SHEET_ID = "1GJ3dpsw2ha2_FZKyS4rHnp-4-jVBxtkdu9AaWvnFUf4"

# Dit werkte vanmiddag en hiermee haal je de data direct binnen zonder fouten
URL_TAFELTENNIS_DB = f"https://google.com{SHEET_ID}/export?format=csv&gid=0"
URL_POULE_HISTORIE = f"https://google.com{SHEET_ID}/export?format=csv&gid=403378546"

try:
    df_db = pd.read_csv(URL_TAFELTENNIS_DB)
    df_poule = pd.read_csv(URL_POULE_HISTORIE)
    st.success("Database succesvol geladen!")
except Exception as e:
    st.error(f"Er gaat iets mis bij het ophalen van de data: {e}")
