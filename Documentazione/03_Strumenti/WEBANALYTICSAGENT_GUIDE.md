# 📊 WebAnalyticsAgent - Guida Completa

Guida passo-passo per utilizzare WebAnalyticsAgent, lo strumento di analisi web avanzato per estrarre, analizzare e visualizzare dati da Google Analytics e web scraping.

---

## 📋 Indice

1. [Panoramica](#panoramica)
2. [Struttura e Componenti](#struttura-e-componenti)
3. [Installazione e Setup](#installazione-e-setup)
4. [Come Usare WebAnalyticsAgent](#come-usare-webanalyticsagent)
5. [Moduli Disponibili](#moduli-disponibili)
6. [Casi d'Uso Pratici](#casi-duso-pratici)
7. [Troubleshooting](#troubleshooting)

---

## Panoramica

**WebAnalyticsAgent** è un'infrastruttura completa per:
- ✅ **Raccogliere dati** da Google Analytics (CSV export)
- ✅ **Analizzare metriche** di traffico, engagement, conversioni
- ✅ **Generare visualizzazioni** automatiche (grafici, report)
- ✅ **Fornire insights strategici** per ottimizzazione SEO/Marketing

### Progettati per:
- **FedericoCalo.dev** - Portfolio & Freelance Services
- **CasaDelleMagnolie.com** - Vacation Rental Property
- **PlayTheEvent.com** - SaaS Event Management Platform

---

## Struttura e Componenti

```
Documentazione/WebAnalyticsAgent/
├── README.md                      # Guida rapida (questo file)
├── analytics_analyzer.py           # Parser di Google Analytics CSV
├── visualize_analytics.py          # Generatore di grafici
├── strategic_analysis.py           # Analisi strategica e raccomandazioni
├── google_analytics_schema.md      # Schema dati GA
└── examples/                       # Esempi di output
    ├── sample_report.json
    ├── charts_output/
    └── strategic_recommendations.txt
```

### Moduli Principali

| Modulo | Funzione | Output |
|--------|----------|--------|
| **analytics_analyzer.py** | Legge CSV di Google Analytics, estrae metriche | JSON strutturato |
| **visualize_analytics.py** | Genera grafici da dati analizzati | 6 PNG charts |
| **strategic_analysis.py** | Analizza trend e fornisce raccomandazioni | Report TXT |

---

## Installazione e Setup

### Step 1: Naviga alla cartella del progetto

```bash
# Per FedericoCalo
cd "Analisi Web Scraping progetti/FedericoCalo"

# Per CasaDelleMagnolie
cd "Analisi Web Scraping progetti/CasaDelleMagnolie"

# Per PlayTheEvent
cd "Analisi Web Scraping progetti/PlayTheEvent"
```

### Step 2: Attiva l'ambiente virtuale

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3: Installa dipendenze (se non presenti)

```bash
pip install -r requirements.txt
```

**Dipendenze necessarie:**
```
requests>=2.28.0
beautifulsoup4>=4.11.0
pandas>=1.5.0
matplotlib>=3.6.0
numpy>=1.23.0
```

---

## Come Usare WebAnalyticsAgent

### 📥 Prerequisito: Esportare Dati da Google Analytics

1. Accedi a **Google Analytics** del tuo progetto
2. Vai a **Reports** → seleziona il periodo desiderato
3. Clicca su **⬇️ Export** → **CSV**
4. Salva il file come **`Istantanea_report.csv`** nella cartella del progetto

**Esempio percorso:**
```
Analisi Web Scraping progetti/FedericoCalo/Istantanea_report.csv
```

---

### 🔍 Step 1: Analizzare i Dati (analytics_analyzer.py)

```bash
python3 analytics_analyzer.py
```

**Cosa fa:**
- Legge `Istantanea_report.csv`
- Estrae metriche principali:
  - **Users** (utenti unici)
  - **Sessions** (sessioni totali)
  - **Pageviews** (pagine visualizzate)
  - **Bounce Rate** (tasso di rimbalzo)
  - **Avg. Session Duration** (durata media sessione)
  - **Conversions** (conversioni)

**Output generato:**
```
✅ analytics_data.json              # Dati strutturati (metadata + metriche)
✅ user_traffic_timeline.json       # Trend utenti nel tempo
✅ device_sessions.json              # Sessioni per dispositivo
✅ page_performance.json             # Performance per pagina
✅ traffic_sources.json              # Distribuzione fonti traffico
```

### 📊 Step 2: Generare Visualizzazioni (visualize_analytics.py)

```bash
python3 visualize_analytics.py
```

**Grafici generati automaticamente:**

1. **📈 Users by Date** - Trend utenti nel tempo
2. **📱 Sessions by Device** - Distribuzione dispositivi (Mobile/Desktop/Tablet)
3. **👁️ Pageviews by Page** - Top pagine più visitate
4. **🔗 Traffic Sources** - Provenienza del traffico (Organic/Direct/Social)
5. **🎯 Conversions Trend** - Trend conversioni nel tempo
6. **⏱️ User Engagement** - Durata media vs bounce rate

**Output:**
```
✅ charts/
   ├── 1_users_timeline.png
   ├── 2_sessions_by_device.png
   ├── 3_pageviews_by_page.png
   ├── 4_traffic_sources.png
   ├── 5_conversions_trend.png
   └── 6_user_engagement.png
```

### 💡 Step 3: Analisi Strategica (strategic_analysis.py)

```bash
python3 strategic_analysis.py
```

**Genera raccomandazioni su:**

1. **SEO Strategy**
   - Keyword opportunities
   - Page optimization priorities
   - Backlink strategy

2. **Content Strategy**
   - Content gaps analysis
   - High-performing content topics
   - Content calendar recommendations

3. **Traffic Optimization**
   - Channel focus areas
   - Conversion funnel improvements
   - Bounce rate reduction tactics

4. **Marketing Channels**
   - Best performing channels
   - Budget allocation suggestions
   - New channel opportunities

5. **Competitive Positioning**
   - Market positioning
   - Differentiation strategy
   - Growth opportunities

**Output:**
```
✅ strategic_recommendations.txt    # Report completo (italiano)
```

---

## Moduli Disponibili

### 1. analytics_analyzer.py

**Funzione principale:**
```python
analyze_analytics(csv_file_path: str) -> dict
```

**Parametri:**
- `csv_file_path`: Percorso al file CSV di Google Analytics

**Estrae:**
```python
{
    "metadata": {
        "export_date": "2024-01-06",
        "report_type": "Google Analytics",
        "date_range": "2024-01-01 to 2024-01-06"
    },
    "summary": {
        "total_users": 1250,
        "total_sessions": 3420,
        "total_pageviews": 8932,
        "bounce_rate": "45.2%",
        "avg_session_duration": "2:34 min"
    },
    "by_date": { ... },
    "by_device": { ... },
    "by_page": { ... },
    "by_source": { ... }
}
```

### 2. visualize_analytics.py

**Funzione principale:**
```python
generate_all_charts(json_file_path: str, output_dir: str)
```

**Personalizzazione:**
```python
# Stili disponibili
styles = ['seaborn-v0_8', 'ggplot', 'bmh', 'fivethirtyeight']

# Colori disponibili
colors = ['steelblue', 'coral', 'seagreen', 'orchid']
```

### 3. strategic_analysis.py

**Funzione principale:**
```python
generate_strategic_analysis(analytics_json: str, output_file: str)
```

**Include:**
- SWOT Analysis
- Growth opportunities
- Risk assessment
- Recommended actions (prioritized)

---

## Casi d'Uso Pratici

### 📌 Caso 1: Analisi Mensile per FedericoCalo.dev

**Obiettivo:** Valutare performance del portfolio

```bash
cd "Analisi Web Scraping progetti/FedericoCalo"
source venv/bin/activate

# 1. Esporta da Google Analytics per il mese scorso
# (Salva come Istantanea_report.csv)

# 2. Analizza
python3 analytics_analyzer.py

# 3. Genera grafici
python3 visualize_analytics.py

# 4. Ottieni raccomandazioni
python3 strategic_analysis.py

# 5. Visualizza report
cat strategic_recommendations.txt
```

**Metriche chiave da monitorare:**
- Trend utenti (crescita?)
- Bounce rate (engagement?)
- Top pagine (cosa interessa ai visitatori?)
- Traffic sources (da dove arrivano clienti?)

---

### 🏡 Caso 2: Analisi Occupancy per CasaDelleMagnolie.com

**Obiettivo:** Correlare traffico web con prenotazioni

```bash
cd "Analisi Web Scraping progetti/CasaDelleMagnolie"
source venv/bin/activate

# 1. Analizza traffico web
python3 analytics_analyzer.py

# 2. Genera visualizzazioni
python3 visualize_analytics.py

# 3. Confronta con dati di occupancy
# (Da financial_manager.py)
python3 financial_manager.py --report occupancy

# 4. Analisi strategica
python3 strategic_analysis.py
```

**Metriche chiave:**
- Pagine dettagli proprietà (views vs prenotazioni)
- Conversion rate (visitor → booking)
- Seasonal trends
- Device type (mobile è importante!)

---

### 🎪 Caso 3: Analisi SaaS per PlayTheEvent.com

**Obiettivo:** Ottimizzare acquisition e retention

```bash
cd "Analisi Web Scraping progetti/PlayTheEvent"
source venv/bin/activate

python3 analytics_analyzer.py
python3 visualize_analytics.py
python3 strategic_analysis.py
```

**Metriche chiave:**
- Signup funnel completion
- Trial to paid conversion
- Feature page performance
- Pricing page bounce rate

---

## Troubleshooting

### ❌ Errore: "No module named 'pandas'"

**Soluzione:**
```bash
# Assicurati di avere attivo il venv
source venv/bin/activate

# Installa dipendenze
pip install pandas matplotlib numpy
```

---

### ❌ Errore: "File 'Istantanea_report.csv' not found"

**Soluzione:**
1. Verifica di aver esportato il file da Google Analytics
2. Controlla che sia salvato nella cartella corretta
3. Verifica il nome esatto del file (case-sensitive)

```bash
# Debug
ls -la Istantanea_report.csv
pwd  # Mostra cartella corrente
```

---

### ❌ Grafici non si generano correttamente

**Soluzione:**
```bash
# Assicurati che matplotlib sia installato
pip install --upgrade matplotlib

# Pulisci i grafici precedenti
rm -rf charts/

# Ri-genera
python3 visualize_analytics.py
```

---

### ❌ Errore durante analisi strategica

**Soluzione:**
```bash
# Verifica che analytics_data.json esista
ls -la analytics_data.json

# Se non esiste, prima lancia analyzer
python3 analytics_analyzer.py

# Poi strategic_analysis
python3 strategic_analysis.py
```

---

## 📈 Best Practices

### ✅ Analisi Regolare
- **Settimanale:** Monitorare trend principali
- **Mensile:** Generare report completo + visualizzazioni
- **Trimestrale:** Analisi strategica + pianificazione

### ✅ Confronto Storico
```bash
# Salva report mensili con data
cp analytics_data.json "analytics_data_2024-01.json"
cp strategic_recommendations.txt "strategic_2024-01.txt"
```

### ✅ Creazione Dashboard
Prendi i JSON generati e importali in:
- Google Sheets (per collaborazione)
- Tableau Public (per visualizzazioni interattive)
- Notion (per team collaboration)

### ✅ Integrazione con Financial Manager
Combina insights web analytics con dati finanziari:
```bash
# Genera entrambi i report
python3 analytics_analyzer.py      # Web traffic
python3 financial_manager.py       # Revenue data

# Confronta risultati per ROI analysis
```

---

## 📚 Riferimenti Correlati

**Guide correlate in Documentazione/:**
- [PROJECT_MANAGEMENT_GUIDE.md](PROJECT_MANAGEMENT_GUIDE.md) - Planning & monitoring
- [TIME_PRODUCTIVITY_GUIDE.md](TIME_PRODUCTIVITY_GUIDE.md) - Automated reporting workflow
- [FINANCIAL_MANAGEMENT_GUIDE.md](FINANCIAL_MANAGEMENT_GUIDE.md) - Correlate web metrics con revenue

**File schema:**
- [google_analytics_schema.md](google_analytics_schema.md) - Struttura dati GA

---

## 🎯 Prossimi Passi

1. **Setup iniziale:** Esporta dati GA e esegui analyzer
2. **Visualizza dati:** Genera grafici per comprensione visuale
3. **Leggi insights:** Analizza raccomandazioni strategiche
4. **Implementa:** Agisci su raccomandazioni prioritarie
5. **Monitora:** Ripeti analisi mensile per tracciare progresso

---

**Ultimo aggiornamento:** 6 Gennaio 2024  
**Versione:** 1.0  
**Autore:** Federico Calò
