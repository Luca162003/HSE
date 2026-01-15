import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
# --- 1. CONFIGURAZIONE ---

logo_path = Image.open("/home/luca/Desktop/Pitone/HSE/logo_scuola.jpg")

# 2. Imposta la configurazione della pagina (deve essere il PRIMO comando Streamlit)
st.set_page_config(
    page_title="HSE Simulation", 
    layout='wide', 
    page_icon= logo_path)
# --- 2. DATI DEL GIOCO ---
keys = ["PROD", "SODD", "REP", "BUDGET", "HSE_P", "HSE_C"]

questions = [
    {
        "text": "Scenario 1: Situazione iniziale in azienda",
        "desc": "L'azienda si trova a dover decidere come allocare il budget annuale per la sicurezza. I macchinari sono vecchi e il morale è basso.",
        "answers": [
            {"label": "Investimento forte su tutto", "delta": [10, 15, 15, -5000, 5, 5]},
            {"label": "Taglio costi radicale", "delta": [0, 0, 0, -25000, 0, 0]},
            {"label": "Intervento mirato sui macchinari", "delta": [0, 0, 0, -15000, 0, 0]},
            {"label": "Nessuna azione per ora", "delta": [0, 0, 0, 0, 0, 0]}
        ]
    },
    {
        "text": "Scenario 2: Gestione di un incidente",
        "desc": "Un operaio è scivolato a causa di una perdita d'olio non segnalata. Non ci sono feriti gravi, ma c'è spavento.",
        "answers": [
            {"label": "Fermo produzione e corso sicurezza", "delta": [15, 20, 15, -10000, 10, 5]},
            {"label": "Pulisco e riparto subito", "delta": [-5, 0, 0, -5000, 0, 0]},
            {"label": "Do la colpa all'operaio", "delta": [-5, 0, 0, -5000, 0, 0]},
            {"label": "Investigazione interna discreta", "delta": [2, 2, 2, -15000, 0, 0]}
        ]
    },
    {
        "text": "Scenario 3: Formazione del personale",
        "desc": "È il momento di pianificare la formazione annuale. Il budget è stretto.",
        "answers": [
            {"label": "Formazione completa per tutti", "delta": [10, 10, 10, -2000, 5, 5]},
            {"label": "Solo obbligatoria per legge", "delta": [0, 2, 2, -5000, 0, 0]},
            {"label": "E-learning economico", "delta": [0, 2, 0, -2000, 0, 0]},
            {"label": "Nessuna formazione extra", "delta": [-5, 0, 0, -2000, 0, 0]}
        ]
    },
    {
        "text": "Scenario 4: Audit finale",
        "desc": "L'ispettore esterno sta arrivando per il controllo qualità e sicurezza.",
        "answers": [
            {"label": "Preparo tutto lo staff (Straordinari)", "delta": [5, 15, 15, -15000, 0, 5]},
            {"label": "Spero vada bene così", "delta": [0, 0, 0, -10000, 0, 0]},
            {"label": "Nascondo i problemi evidenti", "delta": [-5, 0, 5, -10000, 0, 0]},
            {"label": "Corrompo l'ispettore (Rischio!)", "delta": [-10, 5, 10, -25000, 0, 0]}
        ]
    }
]

# --- 3. STATO (MEMORIA) ---
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'stats' not in st.session_state:
    st.session_state.stats = {"PROD": 70, "SODD": 50, "REP": 50, "BUDGET": 50000, "HSE_P": 60, "HSE_C": 60}

def update_stats(delta):
    for i, key in enumerate(keys):
        st.session_state.stats[key] += delta[i]
    st.session_state.q_index += 1

# --- 4. LAYOUT GRAFICO ---

# Intestazione semplice
st.title(" HSE Manager Simulator")
st.markdown("Realizzato da Luca Tognari - Scuola Superiore Sant'Anna")
st.divider()

# -- SE IL GIOCO È FINITO --
if st.session_state.q_index >= len(questions):
    st.success(" Simulazione Completata!")
    
    colA, colB = st.columns([1, 1])
    
    with colA:
        st.subheader("Performance Aziendali")
        # Grafico Radar
        radar_data = {k: v for k, v in st.session_state.stats.items() if k != "BUDGET"}
        df = pd.DataFrame(dict(r=list(radar_data.values()), theta=list(radar_data.keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True, range_r=[0, 120])
        fig.update_traces(fill='toself', marker=dict(size=10), line_width=2)
        # Aggiunge una griglia più densa
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    tickfont=dict(color="black"), # Rende i numeri (0, 20, 40...) neri
                    gridcolor="rgba(0,0,0,0.1)"   # Opzionale: rende le linee dei cerchi grigio chiaro
                ),
                angularaxis=dict(
                    tickfont=dict(color="white")  # Rende i nomi dei KPI (PROD, SODD...) neri
                )
            ),
    paper_bgcolor="rgba(0,0,0,0)", # Sfondo del grafico trasparente
    plot_bgcolor="rgba(0,0,0,0)"
)
        st.plotly_chart(fig, use_container_width=True)

    with colB:
        st.subheader("Budget Finale")
        final_budget = st.session_state.stats["BUDGET"]
        delta_budget = final_budget - 50000
        st.metric("Budget Residuo", f"{final_budget} €", f"{delta_budget} €")
        
        
    st.divider()
    if st.button(" Ricomincia Partita", type="primary"):
            st.session_state.q_index = 0
            st.session_state.stats = {"PROD": 70, "SODD": 50, "REP": 50, "BUDGET": 50000, "HSE_P": 60, "HSE_C": 60}
            st.rerun()

# -- SE IL GIOCO È IN CORSO --
else:
        q = questions[st.session_state.q_index]
        progress = st.session_state.q_index / len(questions)
        
        
        
        st.subheader(q["text"])
        st.write(f"*{q['desc']}*") # Descrizione in corsivo
        
        st.markdown("### Cosa fai?")
        
        # Pulsanti disposti a griglia
        b_col1, b_col2 = st.columns(2)
        ans = q["answers"]
        
        with b_col1:
            if st.button(ans[0]["label"], use_container_width=True): 
                update_stats(ans[0]["delta"])
                st.rerun()
            st.write("") # Spaziatura
            if st.button(ans[2]["label"], use_container_width=True): 
                update_stats(ans[2]["delta"])
                st.rerun()
                
        with b_col2:
            if st.button(ans[1]["label"], use_container_width=True): 
                update_stats(ans[1]["delta"])
                st.rerun()
            st.write("") # Spaziatura
            if st.button(ans[3]["label"], use_container_width=True): 
                update_stats(ans[3]["delta"])
                st.rerun()
        st.progress(progress, text=f"Progresso: {int(progress*100)}%")
        
        # Mostra budget attuale in piccolo
        st.divider()
        st.markdown('opzionale')
        st.caption(f"💰 Budget Attuale: {st.session_state.stats['BUDGET']} €")