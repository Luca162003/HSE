import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# --- 1. CONFIGURAZIONE ---
try:
    logo_path = Image.open("logo_scuola.jpg")
except FileNotFoundError:
    logo_path = "🛡️"

st.set_page_config(
    page_title="HSE Simulation", 
    layout='wide', 
    page_icon=logo_path
)

# --- 2. DATI DEL GIOCO ---
# Ordine metriche: [Produttività, Soddisfazione, Reputazione, Budget, HSE Pratica, HSE Cultura]
keys = ["PROD", "SODD", "REP", "BUDGET", "HSE_P", "HSE_C"]

questions = [
    {
        "text": "Scenario 1: Riscontro Infortuni Ricorrenti",
        "desc":  """Gentile **{nome}**,
\nti scriviamo per segnalarti una situazione critica relativa alla sicurezza sul sito di trattamento delle acque, in particolare per i dipendenti addetti alla verifica quotidiana degli impianti.
Come noto, le operazioni di controllo avvengono all’aperto, spesso in condizioni climatiche avverse, con temperature sotto lo zero e presenza di acqua residua da precipitazioni. Questo contesto genera rischi significativi, tra cui:
* Scivolamento e cadute, dovuti alla formazione di ghiaccio sulle superfici calpestabili;
* Stress termico, causato dal passaggio repentino tra ambienti esterni freddi e locali interni più caldi;
* Esposizione al rumore, nelle aree dove gli impianti sono in funzione.

Abbiamo riscontrato che tali rischi stanno determinando infortuni ricorrenti, compromettendo la sicurezza e il benessere degli operatori. 
Ti invitiamo a prestare la massima attenzione a queste problematiche. Per qualsiasi ulteriore chiarimento o proposta di miglioramento, restiamo a disposizione.

Cordiali saluti,
Ufficio Risorse Umane""",
        "delta_iniziale": [-25, -25, -5, 0, 0, 0],
        "answers": [
            {"label": "Riorganizzazione del lavoro (Turni e sequenze)", "full_text": "Ritengo utile intervenire attraverso una ri-organizzazione del lavoro, ridefinendo l’assegnazione dei turni e la sequenza delle operazioni di verifica.", "delta": [10, 15, 15, -5000, 5, 5]},
            {"label": "Mystery Audit (Controlli a sorpresa)", "full_text": "Suggerisco di introdurre un sistema di Mystery Audit, inviando personale incaricato a svolgere verifiche non annunciate direttamente sul campo.", "delta": [0, 0, 0, -25000, 0, 0]},
            {"label": "Commissione d'indagine e Feedback", "full_text": "Propongo di istituire una Commissione di indagine su eventi critici e attivare un sistema di feedback strutturato ai lavoratori.", "delta": [0, 0, 0, -15000, 0, 0]},
            {"label": "Sospensione lavoratori infortunati", "full_text": "Una possibile soluzione potrebbe essere la sospensione temporanea dalla mansione per quei lavoratori che hanno registrato infortuni ricorrenti.", "delta": [0, 0, 0, 0, 0, 0]}
        ]
    },
    {
        "text": "Scenario 2: Utilizzo Non Corretto dei DPI",
        "desc": """Gentile **{nome}**, 
\nti scriviamo per segnalare una criticità rilevata presso l’impianto di trattamento delle acque, relativa al mancato o non corretto utilizzo dei dispositivi di protezione individuale (DPI).
Tuttavia, abbiamo riscontrato le seguenti criticità:
* Mancato utilizzo di calzature antiscivolo certificate;
* Assenza o uso improprio di guanti termici;
* Omissione della protezione acustica;
* Indumenti non adeguati alle condizioni climatiche.

L’uso corretto dei DPI è fondamentale per la sicurezza degli operatori e per la prevenzione di incidenti sul lavoro. Ti invitiamo a prendere in considerazione questa problematica.

Cordiali saluti,
Ufficio Risorse Umane""",
        "delta_iniziale": [-5, -10, -5, 0, 0, 0],
        "answers": [
            {"label": "Sensibilizzazione e Formazione", "full_text": "Propongo riunioni periodiche per sensibilizzare sull’importanza dei DPI e rivedere la frequenza della formazione obbligatoria.", "delta": [15, 20, 15, -10000, 10, 5]},
            {"label": "Nuova Valutazione dei Rischi", "full_text": "Avviare una nuova valutazione del rischio specifica per analizzare se le attuali misure e i DPI siano adeguati.", "delta": [-5, 0, 0, -5000, 0, 0]},
            {"label": "Aggiornamento Procedure e Firma", "full_text": "Aggiornare le procedure aziendali e prevedere un sistema di firma obbligatoria per attestare la presa visione delle indicazioni.", "delta": [-5, 0, 0, -5000, 0, 0]},
            {"label": "Aggiornamento Piano di Miglioramento", "full_text": "Proporre un aggiornamento del Piano di Miglioramento della sicurezza per includere interventi specifici nel lungo periodo.", "delta": [2, 2, 2, -15000, 0, 0]}
        ]
    },
    {
        "text": "Scenario 3: Assenze alla Formazione DPI III Categoria",
        "desc": """Gentile **{nome}**, 
\ndesidero segnalarle che durante la sessione di formazione programmata in data 18 aprile sull'uso dei DPI di terza categoria (autorespiratori, imbracature, otoprotettori), uno o più partecipanti non si sono presentati senza comunicazione preventiva.

Segnalo questa circostanza per le opportune valutazioni. 

Cordiali saluti""",
        "delta_iniziale": [-10, -15, -10, 0, 0, 0],
        "answers": [
            {"label": "Discussione in Riunione Periodica", "full_text": "Includere la mancata partecipazione nell'ordine del giorno della prossima riunione periodica per discuterne con i rappresentanti.", "delta": [10, 10, 10, -2000, 5, 5]},
            {"label": "Safety Walk e confronto", "full_text": "Organizzare una safety walk per esaminare le condizioni e confrontarsi direttamente con i lavoratori sul campo.", "delta": [0, 2, 2, -5000, 0, 0]},
            {"label": "Analisi correlazione Infortuni", "full_text": "Avviare un'analisi dettagliata per esaminare se vi siano correlazioni tra la mancata formazione e gli incidenti verificatisi.", "delta": [0, 2, 0, -2000, 0, 0]},
            {"label": "Colloqui individuali", "full_text": "Organizzare incontri individuali con ciascun assente per comprendere le ragioni e ribadire l'importanza della formazione.", "delta": [-5, 0, 0, -2000, 0, 0]}
        ]
    },
    {
        "text": "Scenario 4: Malfunzionamento DPI in Addestramento",
        "desc": """Gentile **{nome}**,
\ndurante la sessione di addestramento pratico sull’uso delle imbracature anticaduta, si è verificato un problema tecnico. Un partecipante ha riscontrato un malfunzionamento nella fibbia di serraggio che ha poi ceduto completamente.
L’episodio ha suscitato preoccupazione tra i partecipanti.

Resto a disposizione per ulteriori informazioni.
Cordiali saluti,""",
        "delta_iniziale": [-5, -10, -15, 0, 0, 0],
        "answers": [
            {"label": "Introduzione KPI Formazione", "full_text": "Introdurre dei KPI per monitorare le prestazioni durante la formazione e l'efficacia dei dispositivi.", "delta": [5, 15, 15, -15000, 0, 5]},
            {"label": "Sostituzione immediata", "full_text": "Sospendere temporaneamente la sessione e sostituire il dispositivo difettoso con uno funzionante per proseguire in sicurezza.", "delta": [0, 0, 0, -10000, 0, 0]},
            {"label": "Intervention Cards", "full_text": "Introdurre schede informative su come intervenire in caso di malfunzionamento dei DPI.", "delta": [-5, 0, 5, -10000, 0, 0]},
            {"label": "Organizzazione Safety Day", "full_text": "Organizzare un 'Safety Day' dedicato alla sensibilizzazione e alla gestione delle emergenze sui DPI.", "delta": [-10, 5, 10, -25000, 0, 0]}
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
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- 4. FUNZIONI ---
def apply_delta(delta_list):
    for i, key in enumerate(keys):
        st.session_state.stats[key] += delta_list[i]

# --- 5. INTERFACCIA UTENTE ---

# Schermata di Benvenuto
if not st.session_state.user_name:
    st.title("🛡️ Benvenuto al Simulatore HSE")
    st.markdown("""
    Ciao!
    Benvenuto/a in **HSEGAME**, un gioco volto a stimolare e rafforzare le capacità di Leadership in ambito Health, Safety and Environment (HSE). L’obiettivo del gioco è sensibilizzare il giocatore in merito ai processi decisionali insiti alla gestione HSE.
    \nIn questo gioco, ti muoverai in un contesto organizzativo. Ti saranno presentati degli Eventi, ovvero degli eventi avversi «verosimili», che peggiorano o potrebbero peggiorare le prestazioni HSE (ad esempio, bassa partecipazione agli eventi formativi o incidenti di vario tipo). Dovrai comprendere e interpretare le cause di tali Eventi e implementare degli Interventi, ossia delle risposte organizzative «verosimili» volte a risolvere le cause di ogni singolo Evento (ad esempio, attività di sensibilizzazione o modifica delle procedure). Dovrai scegliere l’Intervento che ritieni più adatto a risolvere le cause dell’Evento tra quattro opzioni. Le tue scelte produrranno degli effetti sulla prestazione HSE.
    L’obiettivo del gioco è migliorare la prestazione HSE della tua organizzazione, stimolando due tipologie di comportamento tra i tuoi collaboratori e le tue collaboratrici:
* Compliance, ossia il rispetto di procedure e istruzioni operative;
* Participation, ossia comportamenti volontari e proattivi per il miglioramento della sicurezza sul luogo di lavoro.
    Tieni presente che le tue scelte influenzeranno anche altre tre statistiche aziendali che è importante preservare: la Soddisfazione del personale, la Produttività aziendale e la Reputazione aziendale.
    \nOra sei pronto/a a giocare!
    """)
    nome = st.text_input("Inserisci il tuo nome per iniziare:")
    if st.button("Inizia Simulazione"):
        if nome:
            st.session_state.user_name = nome
            st.rerun()
        else:
            st.warning("Inserisci un nome!")
    st.stop()

# Header Comune
st.title("🛡️ HSE Manager Simulator")
st.markdown(f"Manager: **{st.session_state.user_name}**")
st.divider()

# Logica Scenari
if st.session_state.q_index < len(questions):
    current_q = questions[st.session_state.q_index]

    # SOTTRAZIONE AUTOMATICA
    if st.session_state.scenario_applied < st.session_state.q_index:
        if "delta_iniziale" in current_q:
            apply_delta(current_q["delta_iniziale"])
        st.session_state.scenario_applied = st.session_state.q_index
        st.rerun()

    # Visualizzazione Domanda
    q = questions[st.session_state.q_index]
    progress = st.session_state.q_index / len(questions)
    
    st.subheader(q["text"])
    
    # Formattazione descrizione
    desc_formattata = q["desc"].format(nome=st.session_state.user_name)
    st.info(desc_formattata)
    
    st.markdown("### Cosa decidi di fare?")
    
    ans = q["answers"]
    

    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        # Opzione 1
        st.markdown(f"**A)** {ans[0]['full_text']}")
        if st.button(f"Scegli: {ans[0]['label']}", key="btn0", use_container_width=True):
            apply_delta(ans[0]["delta"])
            st.session_state.q_index += 1
            st.rerun()
            
        st.markdown("---")
        
        # Opzione 3
        st.markdown(f"**C)** {ans[2]['full_text']}")
        if st.button(f"Scegli: {ans[2]['label']}", key="btn2", use_container_width=True):
            apply_delta(ans[2]["delta"])
            st.session_state.q_index += 1
            st.rerun()

    with col2:
        # Opzione 2
        st.markdown(f"**B)** {ans[1]['full_text']}")
        if st.button(f"Scegli: {ans[1]['label']}", key="btn1", use_container_width=True):
            apply_delta(ans[1]["delta"])
            st.session_state.q_index += 1
            st.rerun()

        st.markdown("---")

        # Opzione 4
        st.markdown(f"**D)** {ans[3]['full_text']}")
        if st.button(f"Scegli: {ans[3]['label']}", key="btn3", use_container_width=True):
            apply_delta(ans[3]["delta"])
            st.session_state.q_index += 1
            st.rerun()

    st.divider()
    # Footer
    col_bar, col_bud = st.columns([3, 1])
    with col_bar:
        st.progress(progress, text=f"Scenario {st.session_state.q_index + 1} di {len(questions)}")
    with col_bud:
        curr_budget = st.session_state.stats['BUDGET']
        color = "green" if curr_budget > 0 else "red"
        st.markdown(f"💰 Budget: **:{color}[{curr_budget} €]**")

# Schermata Finale
else:
    st.success("Simulazione Completata!")
    
    colA, colB = st.columns([1, 1])
    
    with colA:
        st.subheader("Performance Aziendali")
        radar_data = {k: v for k, v in st.session_state.stats.items() if k != "BUDGET"}
        df = pd.DataFrame(dict(r=list(radar_data.values()), theta=list(radar_data.keys())))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself', line_color='#1f77b4')
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 130], dtick=15, tickfont=dict(color="black"),  tickfont_size=12, tickcolor="#000000", linecolor="#000000")))
        st.plotly_chart(fig, use_container_width=True)

    with colB:
        st.subheader("Bilancio Finale")
        final_budget = st.session_state.stats["BUDGET"]
        delta_budget = final_budget - 50000
        st.metric("Budget Residuo", f"{final_budget} €", f"{delta_budget} €")
        
        st.subheader("Impatto Decisionale")
        current_stats = {k: v for k, v in st.session_state.stats.items() if k != "BUDGET"}
        initial_stats = {"PROD": 70, "SODD": 50, "REP": 50, "HSE_P": 60, "HSE_C": 60}
        
        df_comparison = pd.DataFrame({
            "Metrica": list(current_stats.keys()) * 2,
            "Valore": list(initial_stats.values()) + list(current_stats.values()),
            "Stato": ["Iniziale"] * 5 + ["Finale"] * 5
        })
        
        fig_bar = px.bar(df_comparison, x="Metrica", y="Valore", color="Stato", barmode="group")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.divider()
    if st.button("🔄 Ricomincia da capo", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()