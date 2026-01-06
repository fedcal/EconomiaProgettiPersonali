# 📊 PlayTheEvent Analytics - Indice Completo

## 🎯 Panoramica

Questo progetto contiene un'analisi completa e interattiva dei dati di PlayTheEvent con:
- **Dashboard Interattiva** - Visualizzazioni real-time con Plotly/Dash
- **Analisi Narrativa** - Report discorsivo dettagliato
- **Data Processing** - Elaborazione e pulizia dati
- **Reportistica** - Report tecnici e sommari JSON

---

## 📁 Struttura dei File

### 🌐 Dashboard Interattiva
**File**: `analytics_dashboard.py`
- **Descrizione**: Applicazione Dash per visualizzazioni interattive
- **Accesso**: http://localhost:8050 (dopo avvio)
- **Visualizzazioni**:
  - Top 15 Event Types
  - Events Over Time (linea temporale)
  - Events Distribution by Hour
  - Traffic by Operating System
  - Top 10 Countries by Traffic
  - Traffic Sources (pie chart)
  - Top 10 Browsers
  - Top 10 Cities by Traffic
- **Statistiche in Tempo Reale**:
  - Total Events
  - Unique Users
  - Event Types
  - Date Range

### 📖 Analisi Narrativa
**File**: `analisi_narrativa.txt` (16 KB)
- **Descrizione**: Report discorsivo completo in linguaggio naturale
- **Sezioni**:
  - ✅ Sommario Esecutivo
  - ✅ Panoramica Generale
  - ✅ Analisi Comportamento Utenti (segmentazione in 4 livelli)
  - ✅ Analisi Geografica (paesi e città)
  - ✅ Analisi Dispositivi e Browser
  - ✅ Analisi Fonti di Traffico
  - ✅ Pattern Temporali e Orari
  - ✅ Tipologie di Eventi
  - ✅ Metriche di Engagement
  - ✅ Principali Scoperte
  - ✅ Raccomandazioni Strategiche

### 🔧 Data Processing
**File**: `data_processor.py`
- **Descrizione**: Script per elaborazione, pulizia e analisi dati
- **Funzioni**:
  - Caricamento CSV
  - Pulizia dati e validazione
  - Analisi statistica
  - Esportazione sommari JSON
  - Generazione report markdown
- **Output**: 
  - `data_summary.json` (statistiche chiave)
  - `data_analysis_report.md` (report tecnico)

**Esecuzione**:
```bash
python data_processor.py estrazione05012026.csv
```

### 🧮 Analizzatore Narrativo
**File**: `narrative_analyzer.py`
- **Descrizione**: Generatore di report discorsivi
- **Funzioni**:
  - Analisi comportamentale utenti
  - Segmentazione per livelli di attività
  - Insights geografici
  - Pattern temporali
  - Raccomandazioni strategiche
- **Output**: Report narrativo formattato

**Esecuzione**:
```bash
python narrative_analyzer.py estrazione05012026.csv analisi_narrativa.txt
```

### 📋 Report e Dati
**File**: `data_summary.json` (453 bytes)
```json
{
  "timestamp": "2026-01-06T01:13:52.123456",
  "basic_stats": {
    "total_events": 341,
    "unique_users": 20,
    "unique_sessions": 19,
    "event_types": 6
  },
  "geographic": {
    "countries": 5,
    "cities": 12
  },
  "top_events": {...},
  "device_info": {...}
}
```

**File**: `data_analysis_report.md` (742 bytes)
- Report tecnico strutturato in markdown
- Statistiche chiave
- Top events, paesi, sorgenti

**File**: `REPORT_ANALISI_PLAYTHEEVENT.md` (21 KB)
- Report precedente, approfondito
- Analisi dettagliata
- Storiche

---

## 🚀 Come Usare

### 1. Configurazione Ambiente (Una volta)

```bash
# Crea virtual environment
python3 -m venv venv

# Attiva
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt
```

### 2. Avviare la Dashboard Interattiva

```bash
source venv/bin/activate
python analytics_dashboard.py
```

Accedi a: **http://localhost:8050**

### 3. Generare Report Narrativo

```bash
source venv/bin/activate
python narrative_analyzer.py estrazione05012026.csv analisi_narrativa.txt
```

Output: `analisi_narrativa.txt`

### 4. Elaborare Dati

```bash
source venv/bin/activate
python data_processor.py estrazione05012026.csv
```

Output:
- `data_summary.json`
- `data_analysis_report.md`

---

## 📊 Principali Metriche (Snapshot)

| Metrica | Valore |
|---------|--------|
| **Total Events** | 341 |
| **Unique Users** | 20 |
| **Sessions** | 19 |
| **Event Types** | 6 |
| **Countries** | 5 |
| **Cities** | 12 |
| **Events/User** | 17.1 |
| **Main Country** | Italy (71.3%) |
| **Main Source** | Facebook (predominante) |
| **Main OS** | Desktop (predominante) |

---

## 🎯 Insights Chiave

### 👥 Utenti
- **1 Power User** con 234 eventi
- **18 Regular Users** con 5-20 eventi
- Rapporto sessioni/utenti: 0.95 (quasi 1:1)

### 🌍 Geografia
- 71.3% Italia (243 eventi)
- 18.8% USA (64 eventi)
- 6.7% Svezia (23 eventi)

### 📱 Dispositivi
- Forte dominanza **Desktop**
- Browser principale: **Firefox, Chrome**
- OS: **Windows predominante**

### 🔗 Traffico
- Canale principale: **Social** (Facebook)
- Medium: **Referral e Direct**
- Necessaria diversificazione

### ⏰ Temporale
- Picchi durante ore di ufficio (UTC)
- Distribuzione regolare
- Non particolarmente stagionale (dati recenti)

---

## 💡 Raccomandazioni

### Breve Termine
- [ ] Ottimizzare onboarding per new users
- [ ] Analizzare funnel di conversione
- [ ] Re-engagement per casual users

### Medio Termine
- [ ] Diversificare canali di acquisizione
- [ ] Loyalty program per power users
- [ ] Mobile optimization

### Lungo Termine
- [ ] Espansione geografica
- [ ] Marketplace di servizi
- [ ] AI recommendations

---

## 🛠 Troubleshooting

### Porta 8050 già in uso
```python
# In analytics_dashboard.py, cambia:
app.run_server(debug=True, host='0.0.0.0', port=8051)
```

### Dipendenze non installate
```bash
pip install -r requirements.txt --upgrade
```

### Errore nel caricamento CSV
- Verificare che `estrazione05012026.csv` sia nella cartella
- Controllare formato CSV

---

## 📚 Dipendenze Principali

```
pandas==2.1.3           # Data manipulation
plotly==5.18.0          # Interactive visualizations
dash==2.14.2            # Web framework
numpy==1.26.3           # Numerical computing
beautifulsoup4==4.12.3  # Web scraping support
requests==2.31.0        # HTTP library
```

---

## 📞 Contatti

**Generato da**: PlayTheEvent Analytics System
**Data**: 6 gennaio 2026
**Versione**: 1.0

---

## 📝 Note

- I dati sono estratti da Google Analytics 4
- Periodo coperto: 2 giorni (4-5 gennaio 2026)
- Completezza dati: Eccellente
- Possibili variazioni stagionali in periodi lunghi

---

**Last Updated**: 2026-01-06
**Status**: ✅ Production Ready
