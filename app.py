import streamlit as st
import os

DB_FILE = "tafeltennis_db.txt"
POULE_FILE = "poule_historie.txt"

STANDAARD_DATABASE = {
    "plachy,dedek": "10;7;3;❤️ VRIENDJES (HOGE GUNFACTOR);01 november 2026: Plachy was al door en liet Dedek bewust met 3-0 winnen in wedstrijd 6.",
    "darin,plachy": "8;4;4;⚡ TACTISCHE ENERGIEBESPARING;01 november 2026: Plachy spaart 100% zijn energie voor de finale als de poulepot 'dood' is. Darin wint dan makkelijk met 3-0.",
    "plachy,briza": "14;10;4;⚖️ PURE BUSINESS (GUNNEN NIKS);01 november 2026: Plachy leidt ruim (72%), gunt Briza niks. Kan wel door vermoeidheid 1-2 achterkomen, maar wint de 5e set (3-2) op ervaring.",
    "regner,hofman": "12;8;4;❤️ VRIENDJES (HOGE GUNFACTOR);01 november 2026: Hofman was al uitgeschakeld en Regner moest winnen voor de finale. Hofman liet Regner direct met 3-0 winnen zonder set-gegok.",
    "stolfa,regner": "15;5;10;❌ GEEN VRIENDJES (PURE RIVALITEIT);01 november 2026: Regner gunt Stolfa absoluut niks. Vocht tot de laatste set om hem uit te schakelen.",
    "chmela,kern": "6;6;0;📉 TRAININGSMAATJES (DOMINANTIE);02 november 2026: Chmela domineert zwaar. Snelle 3-0 overwinning. Kern verliest supersnel zijn moed en motivatie.",
    "szotek,chalupa": "9;5;4;❌ GEEN VRIENDJES (BURENRUZIE);02 november 2026: Pure burenruzie op de ranglijst. Geen vriendschap, vechten altijd tot de allerlaatste set, ongeacht de poulestand.",
    "byrtus,skacelik": "1;0;1;❤️ VRIENDJES (HOGE GUNFACTOR);02-11-2026: wedstrijd 5 won Skacelik 3-1"
}

def laad_database():
    db = {}
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            for k, v in STANDAARD_DATABASE.items():
                f.write(f"{k}|{v}\n")
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        for lijn in f:
            if "|" in lijn:
                sleutel, data = lijn.strip().split("|", 1)
                p1, p2 = sleutel.split(",")
                parts = data.split(";")
                db[(p1, p2)] = {
                    "totaal": int(parts[0]), "winst_p1": int(parts[1]), "winst_p2": int(parts[2]),
                    "relatie": parts[3], "bewijs": parts[4]
                }
    return db

def herschrijf_database(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        for (p1, p2), data in db.items():
            f.write(f"{p1},{p2}|{data['totaal']};{data['winst_p1']};{data['winst_p2']};{data['relatie']};{data['bewijs']}\n")

def sla_poule_op(datum, speler1, speler2, speler3, speler4):
    poule_leden = sorted([speler1.lower(), speler2.lower(), speler3.lower(), speler4.lower()])
    poule_str = ",".join(poule_leden)
    with open(POULE_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datum}|{poule_str}\n")

def check_poule_historie(s1, s2):
    if not os.path.exists(POULE_FILE):
        return []
    historie = []
    with open(POULE_FILE, "r", encoding="utf-8") as f:
        for lijn in f:
            if "|" in lijn:
                datum, leden_str = lijn.strip().split("|")
                leden = leden_str.split(",")
                if s1.lower() in leden and s2.lower() in leden:
                    historie.append((datum, [l.capitalize() for l in leden]))
    return historie

# ==============================================================================
# STREAMLIT WEBSITE LAY-OUT
# ==============================================================================
st.set_page_config(page_title="Liga Pro Gunfactor Checker", page_icon="🏓", layout="centered")

st.title("🏓 Liga Pro - Gunfactor Checker V1")
st.write("Analyseer live onderlinge relaties, gun-scenario's en poule-historie.")

gun_database = laad_database()

# TABS MAKEN VOOR OVERZICHTELIJKHEID
tab1, tab2 = st.tabs(["📊 Matchup Checker", "📝 Poule Opslaan"])

with tab1:
    st.header("Onderlinge Matchup Controleren")
    
    col1, col2 = st.columns(2)
    with col1:
        naam1 = st.text_input("Speler 1:", key="s1").strip().lower()
    with col2:
        naam2 = st.text_input("Speler 2:", key="s2").strip().lower()
        
    if naam1 and naam2:
        match, omgedraaid = None, False
        sleutel = (naam1, naam2)
        
        if (naam1, naam2) in gun_database:
            match = gun_database[(naam1, naam2)]
        elif (naam2, naam1) in gun_database:
            match = gun_database[(naam2, naam1)]
            sleutel = (naam2, naam1)
            omgedraaid = True
            
        if match:
            # Stats berekenen
            winst_s1 = match["winst_p2"] if omgedraaid else match["winst_p1"]
            winst_s2 = match["winst_p1"] if omgedraaid else match["winst_p2"]
            pct_s1 = (winst_s1 / match["totaal"]) * 100 if match["totaal"] > 0 else 0
            pct_s2 = (winst_s2 / match["totaal"]) * 100 if match["totaal"] > 0 else 0
            
            st.subheader(f"Resultaat: {naam1.capitalize()} vs {naam2.capitalize()}")
            
            # Mooie statistieken kaarten
            c1, c2, c3 = st.columns(3)
            c1.metric(label="Totaal Gespeeld", value=f"{match['totaal']}x")
            c2.metric(label=f"Winst {naam1.capitalize()}", value=f"{winst_s1}x", delta=f"{pct_s1:.1f}%")
            c3.metric(label=f"Winst {naam2.capitalize()}", value=f"{winst_s2}x", delta=f"{pct_s2:.1f}%")
            
            st.info(f"**🧠 Psychologische Relatie:** {match['relatie']}")
            st.warning(f"**📝 Historisch Bewijs:** {match['bewijs']}")
            
            # Poule historie tonen
            poule_matches = check_poule_historie(naam1, naam2)
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
                    match["totaal"] += 1
                    if wie_won.lower() == naam1:
                        if omgedraaid: match["winst_p2"] += 1
                        else: match["winst_p1"] += 1
                    else:
                        if omgedraaid: match["winst_p1"] += 1
                        else: match["winst_p2"] += 1
                        
                    if nieuwe_relatie != "Behoud huidige":
                        match["relatie"] = nieuwe_relatie
                        
                    if u_datum or u_wat:
                        match["bewijs"] += f" | {u_datum}: {u_wat}"
                        
                    gun_database[sleutel] = match
                    herschrijf_database(gun_database)
                    st.success("✅ Succesvol geüpdatet! Ververs de pagina om de nieuwe stats te zien.")
                    
        else:
            st.error(f"Matchup tussen '{naam1.capitalize()}' en '{naam2.capitalize()}' bestaat nog niet.")
            st.subheader("➕ Voeg deze nieuwe spelerscombinatie toe")
            with st.form("new_matchup_form"):
                totaal = st.number_input("Totaal gespeeld:", min_value=1, value=1)
                w1 = st.number_input(f"Winst {naam1.capitalize()}:", min_value=0, value=0)
                w2 = st.number_input(f"Winst {naam2.capitalize()}:", min_value=0, value=0)
                relatie_keuze = st.selectbox("Kies relatie:", ["❤️ VRIENDJES (HOGE GUNFACTOR)", "❌ GEEN VRIENDJES (PURE RIVALITEIT)", "⚡ TACTISCHE ENERGIEBESPARING", "⚖️ PURE BUSINESS (GUNNEN NIKS)"])
                n_datum = st.text_input("Datum/Wedstrijd (bijv. 02-11-2026 wedstrijd 5):")
                n_wat = st.text_input("Wat was de situatie?:")
                
                submit_new = st.form_submit_button("Spelers Opslaan")
                if submit_new:
                    gun_database[(naam1, naam2)] = {
                        "totaal": totaal, "winst_p1": w1, "winst_p2": w2, "relatie": relatie_keuze, "bewijs": f"{n_datum}: {n_wat}"
                    }
                    herschrijf_database(gun_database)
                    st.success("✅ Nieuwe spelers succesvol opgeslagen op je harde schijf!")

with tab2:
    st.header("Volledige 4-mans Poule Opslaan")
    p_datum = st.text_input("Datum/Tijdstip poule (bijv. 02-11-2026 Avond):", key="p_det")
    p1 = st.text_input("Naam Speler 1:", key="p1")
    p2 = st.text_input("Naam Speler 2:", key="p2")
    p3 = st.text_input("Naam Speler 3:", key="p3")
    p4 = st.text_input("Naam Speler 4:", key="p4")
    
    if st.button("Poule Samenstelling Opslaan"):
        if p_datum and p1 and p2 and p3 and p4:
            sla_poule_op(p_datum, p1, p2, p3, p4)
            st.success(f"✅ Poule van {p_datum} succesvol opgeslagen!")
        else:
            st.error("Vul alle velden in om de poule op te slaan.")
