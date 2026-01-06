# PlayTheEvent Analytics Dashboard

Dashboard interattiva per l'analisi dei dati di PlayTheEvent con visualizzazioni Plotly e Dash.

## Contenuto

- **analytics_dashboard.py**: Application Dash per la dashboard interattiva
- **data_processor.py**: Script per l'elaborazione e l'analisi dei dati
- **setup.sh**: Script per configurare l'ambiente
- **requirements.txt**: Dipendenze Python

## Requisiti

- Python 3.8+
- pip (gestore pacchetti Python)

## Installazione Rapida

### Su Linux/macOS:

```bash
chmod +x setup.sh
./setup.sh
```

### Su Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python analytics_dashboard.py
```

### Installazione Manuale:

```bash
# Crea virtual environment
python3 -m venv venv

# Attiva virtual environment
source venv/bin/activate  # Linux/macOS
# oppure
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt

# Avvia la dashboard
python analytics_dashboard.py
```

## Utilizzo

### Avviare la Dashboard

```bash
source venv/bin/activate
python analytics_dashboard.py
```

La dashboard sarà disponibile a: **http://localhost:8050**

### Elaborare i Dati

```bash
source venv/bin/activate
python data_processor.py estrazione05012026.csv
```

Questo genererà:
- `data_summary.json`: Sommario in JSON
- `data_analysis_report.md`: Report dettagliato

## Caratteristiche della Dashboard

### 📊 Visualizzazioni Disponibili

1. **Statistiche Riassuntive**
   - Total Events (Numero totale di eventi)
   - Unique Users (Utenti unici)
   - Event Types (Tipi di eventi)
   - Date Range (Intervallo di date)

2. **Analisi Temporale**
   - Events Over Time (Evoluzione nel tempo)
   - Events Distribution by Hour (Distribuzione oraria)

3. **Analisi degli Eventi**
   - Top 15 Event Types (Tipi di evento più frequenti)
   
4. **Analisi Geografica**
   - Top 10 Countries by Traffic (Paesi principali)
   - Top 10 Cities by Traffic (Città principali)

5. **Analisi Dispositivi**
   - Traffic by Operating System (Sistemi operativi)
   - Top 10 Browsers (Browser principali)

6. **Analisi Sorgenti**
   - Traffic Sources (Sorgenti di traffico)

## Struttura dei Dati

Il CSV deve contenere le seguenti colonne (o un sottoinsieme):

```
user_pseudo_id
event_date
event_time
event_name
ga_session_id
country
city
operating_system
browser
ts_source
ts_medium
ts_campaign
engagement_time_msec
session_engaged
```

## Personalizzazione

### Modificare le Porte

Nel file `analytics_dashboard.py`, modifica la riga finale:

```python
app.run_server(debug=True, host='0.0.0.0', port=8050)
```

Cambia `port=8050` con la porta desiderata.

### Aggiungere Nuove Visualizzazioni

1. Aggiungi un nuovo metodo in `DataAnalyzer` in `analytics_dashboard.py`
2. Aggiungi un `dcc.Graph` nel layout
3. Aggiungi un callback per aggiornare il grafico

Esempio:

```python
def get_my_metric(self):
    """Ritorna la mia metrica"""
    # implementazione
    return data

# Nel layout
dcc.Graph(id="my-chart")

# Callback
@app.callback(
    Output("my-chart", "figure"),
    Input("my-chart", "id")
)
def update_my_chart(id):
    if analyzer is None or analyzer.df is None:
        return {}
    
    data = analyzer.get_my_metric()
    if data.empty:
        return {}
    
    fig = px.bar(data, ...)
    return fig
```

## Troubleshooting

### Virtual Environment non Attivato

```bash
source venv/bin/activate  # Linux/macOS
# oppure
venv\Scripts\activate     # Windows
```

### Porta 8050 già in Uso

Cambia la porta in `analytics_dashboard.py`:

```python
app.run_server(debug=True, host='0.0.0.0', port=8051)  # Usa porta 8051
```

### Errore: "No module named 'dash'"

```bash
pip install -r requirements.txt
```

### Errore: "File not found"

Assicurati che il file CSV sia nella stessa cartella dello script:

```bash
ls -la *.csv  # Linux/macOS
dir *.csv     # Windows
```

## Performance

- **Dataset Piccoli** (< 1M di record): Esecuzione istantanea
- **Dataset Medi** (1-10M di record): Caricamento 1-5 secondi
- **Dataset Grandi** (> 10M di record): Considera di dividere i dati

## Supporto e Contributi

Per problemi o suggerimenti, contatta il team di sviluppo.

## Licenza

Progetto interno - Tutti i diritti riservati

---

**Ultimo aggiornamento**: 2026-01-06
