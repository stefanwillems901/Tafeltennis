import pandas as pd
import streamlit as st
from supabase import create_client, Client

# Pagina-instellingen
st.set_page_config(page_title="Liga Pro Gunfactor Checker V1", page_icon="🏓", layout="wide")

# 1. VERBINDING MAKEN MET SUPABASE
URL_KEY = "NEXT_PUBLIC_SUPABASE_URL" if "NEXT_PUBLIC_SUPABASE_URL" in st.secrets else "LIGA_SUPABASE_URL"
SUPABASE_URL = st.secrets.get(URL_KEY)
SUPABASE_KEY = st.secrets.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase inloggegevens ontbreken in de Secrets!")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Data live ophalen uit de database (Aangepast naar tafeltennis_db!)
try:
    response = supabase.table("tafeltennis_db").select("*").execute()
    data_db = response.data
    df_db = pd.DataFrame(data_db) if data_db else pd.DataFrame(columns=["speler_a", "speler_b", "uitslag", "gunfactor"])
except Exception as e:
    st.error(f"Fout bij het ophalen van data: {e}")
    df_db = pd.DataFrame(columns=["speler_a", "speler_b", "uitslag", "gunfactor"])

# Bereken statistieken voor de kaarten
totaal_wedstrijden = len(df_db)
if not df_db.empty and "gunfactor" in df_db.columns:
    df_db['gunfactor'] = pd.to_numeric(df_db['gunfactor'], errors='coerce')
    gem_gunfactor = df_db['gunfactor'].mean()
    gem_gunfactor = 0.0 if pd.isna(gem_gunfactor) else gem_gunfactor
else:
    gem_gunfactor = 0.0
totaal_poules = 2

# 2. DE EXACTE V0 STYLING (Blauwe Banner & Kaarten)
st.markdown(f"""
    <style>
        #MainMenu, footer, header {{visibility: hidden;}}
        .block-container {{padding-top: 0rem; padding-bottom: 0rem;}}
        .v0-hero-banner {{
            background-color: #0b579d;
            color: white;
            padding: 40px;
            border-radius: 0px 0px 8px 8px;
            margin-bottom: 30px;
            margin-left: -5rem;
            margin-right: -5rem;
            padding-left: 5rem;
        }}
        .v0-title {{ font-size: 42px; font-weight: 800; letter-spacing: -1px; margin-bottom: 5px; }}
        .v0-subtitle {{ font-size: 16px; opacity: 0.9; margin-bottom: 30px; }}
        .stats-container {{ display: flex; gap: 20px; }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(5px);
            padding: 15px 25px;
            border-radius: 12px;
            min-width: 180px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .stat-label {{ font-size: 13px; opacity: 0.8; font-weight: 500; }}
        .stat-value {{ font-size: 36px; font-weight: 700; margin-top: 5px; }}
    </style>
    
    <div class="v0-hero-banner">
        <div class="v0-title">LIGA PRO GUNFACTOR CHECKER <sup>V1</sup></div>
        <div class="v0-subtitle">Registroleer elke wedstrijd, houd de gunfactor in de gaten en leg de poulewinnaars vast. Alles direct opgeslagen in de database.</div>
        <div class="stats-container">
            <div class="stat-card"><div class="stat-label">🏓 Wedstrijden</div><div class="stat-value">{totaal_wedstrijden}</div></div>
            <div class="stat-card"><div class="stat-label">⭐ Gem. gunfactor</div><div class="stat-value">{gem_gunfactor:.1f}</div></div>
            <div class="stat-card"><div class="stat-label">🏆 Poules</div><div class="stat-value">{totaal_poules}</div></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 3. INTERFACE IN TWEE KOLOMMEN
col_links, col_rechts = st.columns(2, gap="large")

with col_links:
    st.markdown("### 🏓 NIEUWE WEDSTRIJD")
    st.caption("Voeg een uitslag toe aan de Tafeltennis DB.")
    
    speler_a = st.text_input("Speler A", key="sa", placeholder="Bijv. Jan")
    speler_b = st.text_input("Speler B", key="sb", placeholder="Bijv. Piet")
    uitslag = st.text_input("Uitslag", key="uits", placeholder="3-1")
    gunfactor_input = st.text_input("Gunfactor (0-10)", key="gun", placeholder="7.5")
    
    if st.button("➕ Wedstrijd toevoegen", type="primary", use_container_width=True):
        if speler_a and speler_b and uitslag and gunfactor_input:
            try:
                schone_gunfactor = float(gunfactor_input.replace(',', '.'))
                
                # Live opslaan in de juiste Supabase database tabel (tafeltennis_db)
                supabase.table("tafeltennis_db").insert({
                    "speler_a": speler_a,
                    "speler_b": speler_b,
                    "uitslag": uitslag,
                    "gunfactor": schone_gunfactor
                }).execute()
                
                st.success("Uitslag succesvol verwerkt!")
                st.rerun()
            except ValueError:
                st.error("Vul een geldig getal in voor de gunfactor.")
            except Exception as e:
                st.error(f"Databasefout tijdens opslaan: {e}")
        else:
            st.error("Vul alle velden in.")

with col_rechts:
    st.markdown("### 📊 TAFELTENNIS DB")
    st.caption(f"{totaal_wedstrijden} wedstrijden geregistreerd")
    
    if not df_db.empty:
        weergave_df = df_db.iloc[::-1].copy()
        
        # Zorg dat de kolommen uit Supabase gematcht worden
        optionele_kolommen = ["speler_a", "speler_b", "uitslag", "gunfactor"]
        weergave_df = weergave_df[[c for c in optionele_kolommen if c in weergave_df.columns]]
        weergave_df.columns = ["Speler A", "Speler B", "Uitslag", "Gunfactor"]
        
        st.dataframe(weergave_df, use_container_width=True, hide_index=True)
    else:
        st.info("De database is momenteel leeg of er zijn geen uitslagen gevonden.")
