# Migration Scripts

Script per la migrazione dei dati finanziari da JSON a MySQL.

## Setup

```bash
cd migration
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## Configurazione

Assicurati che il file `.env` nella root del progetto contenga:

```env
DB_USERNAME=root
DB_PASSWORD=your_password
```

## Esecuzione

```bash
python3 migrate_data.py
```

## Cosa fa lo script

1. Si connette al database MySQL `management_economy`
2. Carica i file JSON da:
   - `../../Analisi Web Scraping progetti/FedericoCalo/financial_data.json`
   - `../../Analisi Web Scraping progetti/CasaDelleMagnolie/financial_data.json`
   - `../../Analisi Web Scraping progetti/PlayTheEvent/financial_data.json`
3. Inserisce i dati nelle tabelle:
   - `projects`
   - `one_time_costs`
   - `recurring_costs`
   - `revenue_streams`
   - `bookings` (per CasaDelleMagnolie)
4. Calcola automaticamente commissioni e ricavi netti per le prenotazioni

## Note

- Lo script è idempotente: può essere eseguito più volte senza creare duplicati
- I progetti esistenti vengono riconosciuti tramite il campo `code`
- Le date devono essere in formato `YYYY-MM-DD`
- Gli importi sono in Euro (EUR)
