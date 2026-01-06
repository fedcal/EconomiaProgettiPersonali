# Google Analytics - Guida Utilizzo

Questo progetto include strumenti di analisi per i dati di Google Analytics esportati.

## File Disponibili

### Script

- **`analytics_analyzer.py`** - Analizza i CSV di Google Analytics e genera report testuali
- **`visualize_analytics.py`** - Crea grafici e visualizzazioni dai dati

### Output Generati

- **`analytics_report.txt`** - Report testuale completo con statistiche
- **`analytics_summary.json`** - Dati aggregati in formato JSON
- **`analytics_*.png`** - 6 grafici di visualizzazione

## Come Usare

### 1. Esportare Dati da Google Analytics

1. Vai su **Google Analytics** (https://analytics.google.com/)
2. Seleziona la proprietà **angular-casa-delle-magnolie**
3. Vai su **Reports** > **Snapshot**
4. In alto a destra, clicca sull'icona **Download** (freccia verso il basso)
5. Seleziona **Export to CSV**
6. Salva il file come `Istantanea_report.csv` in questa cartella

### 2. Analizzare i Dati

```bash
# Attiva l'ambiente virtuale
source venv/bin/activate

# Genera report testuale e JSON
python3 analytics_analyzer.py

# Genera grafici
python3 visualize_analytics.py
```

## Output Generato

### Report Testuale (`analytics_report.txt`)

```
================================================================================
REPORT ANALYTICS - casadellemagnolie.com
================================================================================

Periodo analizzato: 2025-12-06 - 2026-01-02
Durata: 28 giorni

UTENTI
--------------------------------------------------------------------------------
Utenti attivi totali: 55
Nuovi utenti: 55
Utenti di ritorno: 0
Media utenti giornalieri: 1.96
Picco utenti: 23 (giorno 23)
Trend: crescita
...
```

### Grafici Generati

1. **`analytics_daily_users.png`** - Trend utenti attivi giornalieri
2. **`analytics_traffic_sources.png`** - Distribuzione sorgenti traffico (pie chart)
3. **`analytics_geography.png`** - Distribuzione geografica utenti (bar chart)
4. **`analytics_top_pages.png`** - Top 10 pagine più visualizzate
5. **`analytics_user_trends.png`** - Trend utenti 30/7/1 giorni
6. **`analytics_events.png`** - Distribuzione eventi

### JSON Summary (`analytics_summary.json`)

Dati strutturati in JSON per ulteriori elaborazioni:

```json
{
  "period": {
    "start": "2025-12-06",
    "end": "2026-01-02",
    "duration_days": 28
  },
  "users": {
    "total_active_users": 55,
    "total_new_users": 55,
    "returning_users": 0,
    "avg_daily_users": 1.96,
    "peak_day": 23,
    "peak_day_users": 23,
    "growth_trend": "crescita"
  },
  "traffic_sources": {
    "new_users_by_source": {
      "Organic Social": 32,
      "Direct": 22,
      "Organic Search": 1
    },
    ...
  }
}
```

## Analisi Periodiche

Per monitorare il sito nel tempo:

1. **Settimanale/Mensile**: Esporta nuovi dati da Google Analytics
2. **Confronto**: Rinomina i vecchi file (es. `analytics_report_2026-01.txt`)
3. **Rigenera**: Lancia gli script con i nuovi dati
4. **Archivia**: Mantieni lo storico di tutti gli export

## Struttura Dati CSV

Il CSV esportato da Google Analytics contiene:

- Utenti attivi giornalieri
- Nuovi utenti
- Durata media coinvolgimento
- Sorgenti traffico (Social, Direct, Search)
- Distribuzione geografica
- Top pagine visualizzate
- Eventi tracciati
- Retention e fidelizzazione

## Note

- Gli script funzionano con export "Istantanea report" da Google Analytics 4
- Assicurati che il CSV mantenga il nome `Istantanea_report.csv`
- Per periodi diversi, esporta un nuovo CSV dal pannello Analytics

## Troubleshooting

**Problema**: Script non trova il CSV
- **Soluzione**: Assicurati che il file si chiami esattamente `Istantanea_report.csv`

**Problema**: Grafici non generati
- **Soluzione**: Verifica che matplotlib sia installato: `pip install matplotlib`

**Problema**: Dati mancanti nei report
- **Soluzione**: Il CSV potrebbe non contenere tutti i dati. Verifica l'export da Analytics.
