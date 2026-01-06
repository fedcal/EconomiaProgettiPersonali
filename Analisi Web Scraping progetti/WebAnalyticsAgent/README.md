# 🤖 Web Analytics Agent

Agente autonomo e intelligente per l'analisi completa dei dati web analytics con generazione automatica di report dettagliati.

## 🎯 Caratteristiche Principali

### 📊 Moduli di Analisi

1. **Traffic Analyzer** - Analisi del traffico web
   - Total sessions, pageviews, visitors
   - Bounce rate, session duration
   - Top pages, traffic sources
   - Hourly/daily trends

2. **User Analyzer** - Analisi del comportamento utenti
   - Segmentazione utenti
   - User retention
   - Lifetime value
   - User type distribution

3. **Conversion Analyzer** - Analisi delle conversioni
   - Conversion rate e value
   - Conversion funnel
   - Abandoned carts
   - Top conversion pages

4. **Engagement Analyzer** - Analisi dell'engagement
   - Time on page/site
   - Scroll depth
   - Video engagement
   - Form interactions

5. **Geographic Analyzer** - Analisi geografica
   - Distribuzione per paese/regione/città
   - Performance geografica
   - Regional insights

6. **Device Analyzer** - Analisi dispositivi
   - Device types, OS, browsers
   - Screen resolutions
   - Device performance

7. **Behavioral Analyzer** - Analisi comportamentale
   - User flow
   - Event patterns
   - Session types
   - Anomaly detection

### 📝 Formati Report

- **HTML** - Report interattivo con stili
- **Markdown** - Formato testuale pulito
- **JSON** - Formato dati strutturato
- **PDF** - Documento imprimibile (in sviluppo)

### 💾 Esportazione

- **JSON** - Formato dati completo
- **CSV** - Formato tabulare

---

## 🚀 Quick Start

### 1. Preparazione

```bash
# Entra nella cartella
cd WebAnalyticsAgent

# Crea virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# oppure
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install pandas numpy
```

### 2. Uso da CLI

```bash
# Analizza un file CSV e genera HTML
python cli.py --data my_analytics.csv --type csv --format html

# Analizza e genera tutti i formati di report
python cli.py --data data.csv --format all

# Analizza e esporta risultati
python cli.py --data data.csv --export json

# Usa configurazione personalizzata
python cli.py --config config.json --data data.csv
```

### 3. Uso Interattivo

```bash
# Avvia modalità interattiva
python cli.py --interactive

# Comandi disponibili:
# add <name> <type> <path>  - Aggiungi fonte dati
# analyze                   - Analizza tutte le fonti
# report <source> <format>  - Genera report
# export <format>           - Esporta risultati
# status                    - Mostra stato
```

### 4. Uso Programmato

```python
from web_analytics_agent import WebAnalyticsAgent

# Inizializza agente
agent = WebAnalyticsAgent(config_file='config.json')

# Aggiungi fonte dati
agent.add_data_source('my_site', 'csv', 'analytics.csv')

# Analizza
agent.analyze_all_sources()

# Genera report
agent.generate_report('my_site', 'html')
agent.generate_all_reports(['html', 'json'])

# Esporta
agent.export_results('json', './exports')

# Ottieni sommario
summary = agent.get_summary()
```

---

## 📁 Struttura Cartelle

```
WebAnalyticsAgent/
├── web_analytics_agent.py      # Agente principale
├── cli.py                       # Interfaccia CLI
├── config.json                  # Configurazione
│
├── analyzers/                   # Moduli di analisi
│   ├── base_analyzer.py
│   ├── traffic_analyzer.py
│   ├── user_analyzer.py
│   ├── conversion_analyzer.py
│   ├── engagement_analyzer.py
│   ├── geographic_analyzer.py
│   ├── device_analyzer.py
│   └── behavioral_analyzer.py
│
├── reports/                     # Generatori report
│   └── report_generator.py
│
├── exporters/                   # Esportatori dati
│   └── data_exporter.py
│
├── agents/                      # Agenti specializzati (future)
├── utils/                       # Utility functions
│
├── data/                        # Cartella input (crea manualmente)
├── reports/                     # Report generati
├── exports/                     # Dati esportati
│
└── README.md                    # Documentazione
```

---

## 📊 Esempio File Input

### CSV Format

```csv
date,sessions,users,pageviews,bounce_rate,avg_duration,source
2026-01-01,100,80,250,45.0,120,organic
2026-01-02,120,95,300,42.0,130,social
```

### GA4 Export

File CSV esportato direttamente da Google Analytics 4

### JSON Format

```json
{
  "date": "2026-01-01",
  "sessions": 100,
  "users": 80,
  "events": [
    {"event": "page_view", "count": 250},
    {"event": "click", "count": 150}
  ]
}
```

---

## ⚙️ Configurazione

Modifica `config.json` per personalizzare:

```json
{
  "analysis_config": {
    "modules": ["traffic", "users", "conversions", ...],
    "enable_anomaly_detection": true
  },
  "report_config": {
    "output_dir": "./reports",
    "formats": ["html", "markdown", "json"]
  },
  "thresholds": {
    "high_bounce_rate": 50.0,
    "low_conversion_rate": 2.0
  }
}
```

---

## 📈 Output Example

### HTML Report
- Layout responsive
- Metriche chiave highlighted
- Tabelle dati ordinabili
- Grafici embed

### Markdown Report
- Sezioni ben organizzate
- Tabelle formattate
- Facile da condividere
- Integrabile in Wiki

### JSON Export
- Struttura dati completa
- Importabile in sistemi esterni
- Schema consistente

---

## 🔧 Troubleshooting

### Errore: "No module named pandas"
```bash
pip install pandas numpy
```

### File non trovato
- Verificare percorso assoluto
- Controllare permessi lettura

### Report non generato
- Controllare cartella output
- Verificare spazio disco
- Controllare log errori

---

## 🎓 Casi d'Uso

1. **Dashboard Automatica** - Analisi giornaliera con report auto-generati
2. **Audit Site** - Analisi completa per audit web
3. **Performance Tracking** - Monitoraggio KPI nel tempo
4. **Competitive Analysis** - Analisi vs competitor
5. **User Behavior** - Studi del comportamento utenti

---

## 📞 Supporto

Per issues, feature requests o domande:
1. Controlla la documentazione
2. Verifica i log
3. Consulta gli esempi

---

## 📝 Note Versione

**v1.0.0** - Initial Release
- ✅ 7 moduli di analisi
- ✅ 4 formati report
- ✅ 2 formati esportazione
- ✅ CLI interattiva
- ✅ API programmabile

---

**Created**: 2026-01-06  
**Last Updated**: 2026-01-06  
**License**: Internal Use
