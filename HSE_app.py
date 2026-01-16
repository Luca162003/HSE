import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# --- 1. CONFIGURAZIONE ---
try:
    logo_path = Image.open("logo_scuola.jpg")
except:
    logo_path = "🛡️"

st.set_page_config(
    page_title="HSE Simulation", 
    layout='wide', 
    page_icon=logo_path
)

# --- 2. DATI DEL GIOCO ---
keys = ["PROD", "SODD", "REP", "BUDGET", "HSE_P", "HSE_C"]

questions = [
    {
        "text": "Scenario 1: Situazione iniziale in azienda",
        "desc": "L'azienda si trova a dover decidere come allocare il budget annuale per la sicurezza. I macchinari sono vecchi e il morale è basso.",
        "delta_iniziale": [-25,-25,-5,0,0,0],
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
        "delta_iniziale": [-5,-10,-5,0,0,0],
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
        "delta_iniziale": [-10,-15,-10,0,0,0],
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
        "delta_iniziale": [-5,-10,-15,0,0,0],
        "answers": [
            {"label": "Preparo tutto lo staff (Straordinari)", "delta": [5, 15, 15, -15000, 0, 5]},
            {"label": "Spero vada bene così", "delta": [0, 0, 0, -10000, 0, 0]},
            {"label": "Nascondo i problemi evidenti", "delta": [-5, 0, 5, -10000, 0, 0]},
            {"label": "Corrompo l'ispettore (Rischio!)", "delta": [-10, 5, 10, -25000, 0, 0]}
        ]
    }
]

# --- 3. INIZIALIZZAZIONE SESSION STATE ---
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'stats' not in st.session_state:
    st.session_state.stats = {"PROD": 70, "SODD": 50, "REP": 50, "BUDGET": 50000, "HSE_P": 60, "HSE_C": 60}
if 'scenario_applied' not in st.session_state:
    st.session_state.scenario_applied = -1

# --- 4. FUNZIONI ---
def apply_delta(delta_list):
    for i, key in enumerate(keys):
        st.session_state.stats[key] += delta_list[i]

# --- 5. LOGICA DI GIOCO ---
if st.session_state.q_index < len(questions):
    current_q = questions[st.session_state.q_index]

    # SOTTRAZIONE AUTOMATICA (Appena appare la domanda)
    if st.session_state.scenario_applied < st.session_state.q_index:
        if "delta_iniziale" in current_q: # CORRETTO: ora coincide con la chiave nel dizionario
            apply_delta(current_q["delta_iniziale"])
        st.session_state.scenario_applied = st.session_state.q_index
        st.rerun()

# --- 6. INTERFACCIA ---
if 'user_name' not in st.session_state:
    st.title("Benvenuto al Simulatore HSE")
    nome = st.text_input("Inserisci il tuo nome per iniziare:")
    if st.button("Inizia Simulazione"):
        if nome:
            st.session_state.user_name = nome
            st.rerun()
        else:
            st.warning("Inserisci un nome!")
    st.stop()
st.title("🛡️ HSE Manager Simulator")
st.markdown("Realizzato da Luca Tognari - Scuola Superiore Sant'Anna")
st.divider()

if st.session_state.q_index >= len(questions):
    st.success("🎉 Simulazione Completata!")
    
    colA, colB = st.columns([1, 1])
    with colA:
        st.subheader("Performance Aziendali")
        radar_data = {k: v for k, v in st.session_state.stats.items() if k != "BUDGET"}
        df = pd.DataFrame(dict(r=list(radar_data.values()), theta=list(radar_data.keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True, range_r=[0, 120])
        fig.update_traces(fill='toself', marker=dict(size=10), line_width=2)
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, tickfont=dict(color="black"), gridcolor="rgba(0,0,0,0.1)"),
                angularaxis=dict(tickfont=dict(color="white"))
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with colB:
        st.subheader("Budget Finale")
        final_budget = st.session_state.stats["BUDGET"]
        delta_budget = final_budget - 50000
        st.metric("Budget Residuo", f"{final_budget} €", f"{delta_budget} €")
        st.subheader("Statistiche generali")
        current_stats = {k: v for k, v in st.session_state.stats.items() if k != "BUDGET"}
        initial_stats = {"PROD": 70, "SODD": 50, "REP": 50, "HSE_P": 60, "HSE_C": 60}
        df_comparison = pd.DataFrame({
            "Iniziale": initial_stats,
            "Attuale": current_stats
        })

        st.bar_chart(df_comparison, width=500, y_label='Valore', stack=False, sort=False)
        
    st.divider()
    if st.button("🔄 Gioca ancora", type="primary"):
        st.session_state.q_index = 0
        st.session_state.stats = {"PROD": 70, "SODD": 50, "REP": 50, "BUDGET": 50000, "HSE_P": 60, "HSE_C": 60}
        st.session_state.scenario_applied = -1
        st.rerun()

else:
    q = questions[st.session_state.q_index]
    progress = st.session_state.q_index / len(questions)
    
    st.subheader(q["text"])
    st.info(q['desc']) # Box blu per la descrizione
    
    st.markdown("### Cosa fai?")
    b_col1, b_col2 = st.columns(2)
    ans = q["answers"]
    
    with b_col1:
        if st.button(ans[0]["label"], use_container_width=True, key="btn0"): 
            apply_delta(ans[0]["delta"])
            st.session_state.q_index += 1
            st.rerun()
        if st.button(ans[2]["label"], use_container_width=True, key="btn2"): 
            apply_delta(ans[2]["delta"])
            st.session_state.q_index += 1
            st.rerun()
            
    with b_col2:
        if st.button(ans[1]["label"], use_container_width=True, key="btn1"): 
            apply_delta(ans[1]["delta"])
            st.session_state.q_index += 1
            st.rerun()
        if st.button(ans[3]["label"], use_container_width=True, key="btn3"): 
            apply_delta(ans[3]["delta"])
            st.session_state.q_index += 1
            st.rerun()

    st.divider()
    st.progress(progress, text=f"Progresso: {int(progress*100)}%")
    st.caption(f"💰 Budget Attuale: {st.session_state.stats['BUDGET']} €")