import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ==============================================================================
# LIVE GOOGLE SHEETS VERBINDING
# ==============================================================================
conn = st.connection("gsheets", type=GSheetsConnection)

# Altijd live data ophalen bij het opstarten
df_db = conn.read(worksheet="tafeltennis_db", ttl=0)
df_historie = conn.read(worksheet="poule_historie", ttl=0)

# Standaard data back-up voor als de Google Sheet helemaal leeg is
STANDAARD_DATABASE = [
    {"Speler 1": "plachy", "Speler 2": "dedek", "totaal": 10, "winst_p1": 7, "winst_p2": 3, "Status": "❤️ VRIENDJES (HOGE GUNFACTOR)", "bewijs": "01 november 2026: Plachy was al door en liet Dedek bewust met 3-0 winnen in wedstrijd 6."},
    {"Speler 1": "darin", "Speler 2": "plachy", "totaal": 8, "winst_p1": 4, "winst_p2": 4, "Status": "⚡ TACTISCHE ENERGIEBESPARING", "bewijs": "01 november 2026: Plachy spaart 100% zijn energie voor de finale als de poulepot 'dood' is. Darin wint dan makkelijk met 3-0."},
    {"Speler 1": "plachy", "Speler 2": "briza", "totaal": 14, "winst_p1": 10, "winst_p2": 4, "Status": "⚖️ PURE BUSINESS (GUNNEN NIKS)", "bewijs": "01 november 2026: Plachy leidt ruim (72%), gunt Briza niks. Kan wel door vermoeidheid 1-2 achterkomen, maar wint de 5e set (3-2) op ervaring."},
    {"Speler 1": "regner", "Speler 2": "hofman", "totaal": 12, "winst_p1": 8, "winst_p2": 4, "Status": "❤️ VRIENDJES (HOGE GUNFACTOR)", "bewijs": "01 november 2026: Hofman was al uitgeschakeld en Regner moest winnen voor de finale. Hofman liet Regner direct met 3-0 winnen zonder set-gegok."},
    {"Speler 1": "stolfa", "Speler 2": "regner", "totaal": 15, "winst_p1": 5, "winst_p2": 10, "Status": "❌ GEEN VRIENDJES (PURE RIVALITEIT)", "bewijs": "01 november 2026: Regner gunt Stolfa absoluut niks. Vocht tot de laatste set om hem uit te schakelen."},
    {"Speler 1": "chmela", "Speler 2": "kern", "totaal": 6, "winst_p1": 6, "winst_p2": 0, "Status": "📉 TRAININGSMAATJES (DOMINANTIE)", "bewijs": "02 november 2026: Chmela domineert zwaar. Snelle 3-0 overwinning. Kern verliest supersnel his moed en motivatie."},
    {"Speler 1": "szotek", "Speler 2": "chalupa", "totaal": 9, "winst_p1": 5, "winst_p2": 4, "Status": "❌ GEEN VRIENDJES (BURENRUZIE)", "bewijs": "02 november 2026: Pure burenruzie op de ranglijst. Geen vriendschap, vechten altijd tot de allerlaatste set, ongeacht de poulestand."},
    {"Speler 1": "byrtus", "Speler 2": "skacelik", "totaal": 1, "winst_p1": 0, "winst_p2": 1, "Status": "❤️ VRIENDJES (HOGE GUNFACTOR)", "bewijs": "02-11-2026: wedstrijd 5 won Skacelik 3-1"}
]

if df_db.empty or len(df_db) <= 1:
    df_db = pd.DataFrame(STANDAARD_DATABASE)
    conn.update(worksheet="tafeltennis_db", data=df_db)

def check_poule_historie_sheets(s1, s2):
    df_hist_live = conn.read(worksheet="poule_historie", ttl=0)
    if df_hist_live.empty:
        return []
    historie = []
    for _, rij in df_hist_live.iterrows():
        if pd.isna(rij["Datum"]) or pd.isna(rij["Spelers"]):
            continue
        leden = [l.strip().lower() for l in str(rij["Spelers"]).split(",")]
        if s1.lower() in leden and s2.lower() in leden:
            historie.append((rij["Datum"], [l.capitalize() for l in leden]))
    return historie

# ==============================================================================
# STREAMLIT LAY-OUT
# ==============================================================================
st.set_page_config(page_title="Liga Pro Gunfactor Checker", page_icon="📓", layout="centered")
st.title("🏓 Liga Pro - Gunfactor Checker V1")
st.write("Analyseer live onderlinge relaties, gun-scenario's en poule-historie.")

tab1, tab2 = st.tabs(["📊 Matchup Checker", "📝 Poule Opslaan"])

# TAB 1: MATCHUP CHECKER
with tab1:
    st.header("Onderlinge Matchup Controleren")
    col1, col2 = st.columns(2)
    with col1:
        naam1 = st.text_input("Speler 1:", key="s1").strip().lower()
    with col2:
        naam2 = st.text_input("Speler 2:", key="s2").strip().lower()
        
    if naam1 and naam2:
        df_db = conn.read(worksheet="tafeltennis_db", ttl=0)
        match_row = None
        omgedraaid = False
        
        if not df_db.empty:
            idx = df_db[(df_db["Speler 1"].str.lower() == naam1) & (df_db["Speler 2"].str.lower() == naam2)].index
            if not idx.empty:
                match_row = idx
            else:
                idx = df_db[(df_db["Speler 1"].str.lower() == naam2) & (df_db["Speler 2"].str.lower() == naam1)].index
                if not idx.empty:
                    match_row = idx
                    omgedraaid = True
            
        if match_row is not None:
            totaal = int(df_db.loc[match_row, "totaal"].values[0])
            winst_p1 = int(df_db.loc[match_row, "winst_p1"].values[0])
            winst_p2 = int(df_db.loc[match_row, "winst_p2"].values[0])
            relatie = str(df_db.loc[match_row, "Status"].values[0])
            bewijs = str(df_db.loc[match_row, "bewijs"].values[0]) if pd.notna(df_db.loc[match_row, "bewijs"].values[0]) else ""
            
            winst_s1 = winst_p2 if omgedraaid else winst_p1
            winst_s2 = winst_p1 if omgedraaid else winst_p2
            pct_s1 = (winst_s1 / totaal) * 100 if totaal > 0 else 0
            pct_s2 = (winst_s2 / totaal) * 100 if totaal > 0 else 0
            
            st.subheader(f"Resultaat: {naam1.capitalize()} vs {naam2.capitalize()}")
            c1, c2, c3 = st.columns(3)
            c1.metric(label="Totaal Gespeeld", value=f"{totaal}x")
            c2.metric(label=f"Winst {naam1.capitalize()}", value=f"{winst_s1}x", delta=f"{pct_s1:.1f}%")
            c3.metric(label=f"Winst {naam2.capitalize()}", value=f"{winst_s2}x", delta=f"{pct_s2:.1f}%")
            
            st.info(f"**🧠 Psychologische Relatie:** {relatie}")
            st.warning(f"**📝 Historisch Bewijs:** {bewijs}")
            
            poule_matches = check_poule_historie_sheets(naam1, naam2)
            if poule_matches:
                st.subheader("📅 Eerder samen in de poule gezien:")
                for dt, leden in poule_matches:
                    st.write(f"• **{dt}**: Poule met *{', '.join(leden)}*")
            
            st.markdown("---")
            st.subheader("🔄 Nieuwe uitslag/data toevoegen")
            
            with st.form("update_form"):
                wie_won = st.selectbox("Wie heeft de nieuwe pot gewonnen?", [naam1.capitalize(), naam2.capitalize()])
                nieuwe_relatie = st.selectbox("Pas relatiestatus aan (optioneel):", ["Behoud huidige", "❤️ VRIENDJES (HOGE GUNFACTOR)", "❌ GEEN VRIENDJES (PURE RIVALITEIT)", "⚡ TACTISCHE ENERGIEBESPARING", "⚖️ PURE BUSINESS (GUNNEN NIKS)"])
                u_datum = st.text_input("Welke datum/wedstrijd? (bijv. 02-11-2026 wedstrijd 6)")
                u_wat = st.text_input("Wat was de situatie? (bijv. Liet hem expres winnen)")
                
                submit_update = st.form_submit_button("Uitslag Toevoegen & Opslaan")
                if submit_update:
                    # Haal live de allernieuwste data op
                    df_db_live = conn.read(worksheet="tafeltennis_db", ttl=0)
                    
                    # Zoek de rij opnieuw op in de live dataframe om index-fouten te voorkomen
                    live_idx = df_db_live[(df_db_live["Speler 1"].str.lower() == naam1) & (df_db_live["Speler 2"].str.lower() == naam2)].index
                    live_omgedraaid = False
                    if live_idx.empty:
                        live_idx = df_db_live[(df_db_live["Speler 1"].str.lower() == naam2) & (df_db_live["Speler 2"].str.lower() == naam1)].index
                        live_omgedraaid = True
                    
                    if not live_idx.empty:
                        row_idx = live_idx[0]
                        huidig_totaal = int(df_db_live.at[row_idx, "totaal"])
                        huidig_w1 = int(df_db_live.at[row_idx, "winst_p1"])
                        huidig_w2 = int(df_db_live.at[row_idx, "winst_p2"])
                        huidig_bewijs = str(df_db_live.at[row_idx, "bewijs"]) if pd.notna(df_db_live.at[row_idx, "bewijs"]) else ""
                        
                        df_db_live.at[row_idx, "totaal"] = huidig_totaal + 1
                        if wie_won.lower() == naam1:
                            if live_omgedraaid: df_db_live.at[row_idx, "winst_p2"] = huidig_w2 + 1
                            else: df_db_live.at[row_idx, "winst_p1"] = huidig_w1 + 1
                        else:
                            if live_omgedraaid: df_db_live.at[row_idx, "winst_p1"] = huidig_w1 + 1
                            else: df_db_live.at[row_idx, "winst_p2"] = huidig_w2 + 1
                            
                        if nieuwe_relatie != "Behoud huidige":
                            df_db_live.at[row_idx, "Status"] = nieuwe_relatie
                            
                        if u_datum or u_wat:
                            df_db_live.at[row_idx, "bewijs"] = f"{huidig_bewijs} | {u_datum}: {u_wat}".strip(" | ")
                            
                        conn.update(worksheet="tafeltennis_db", data=df_db_live)
                        st.success("✅ Succesvol live opgeslagen in Google Sheets! Ververs de pagina om de nieuwe stats te zien.")
                        st.balloons()
                    else:
                        st.error("Matchup kon live niet gevonden worden.")
                    
        else:
            st.error(f"Matchup tussen '{naam1.capitalize()}' en '{naam2.capitalize()}' bestaat nog niet.")
            st.subheader("➕ Voeg deze nieuwe spelerscombinatie toe")
            with st.form("new_matchup_form"):
                totaal_nieuw = st.number_input("Totaal gespeeld:", min_value=1, value=1)
