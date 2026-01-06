# Federico Calò Portfolio Scraper

Web scraper per estrarre dati dal portfolio professionale di Federico Calò (https://federicocalo.dev).

## Descrizione

Questo scraper estrae informazioni strutturate dal sito web personale di Federico Calò, inclusi:

- **Certificazioni**: Titoli, organizzazioni, date e immagini
- **Esperienza professionale**: Ruoli, aziende, periodi e descrizioni
- **Educazione**: Titoli di studio, istituzioni e anni
- **Competenze tecniche**: Linguaggi di programmazione, framework e tecnologie
- **Informazioni di contatto**: Email, GitHub, LinkedIn e altri link social

## Requisiti

- Python 3.8+
- pip (gestore pacchetti Python)

## Installazione

1. Crea un ambiente virtuale:
```bash
python3 -m venv venv
```

2. Attiva l'ambiente virtuale:
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## Utilizzo

Esegui lo scraper:
```bash
python federicocalo_scraper.py
```

I dati estratti verranno salvati in `federicocalo_data.json`.

## Output

Lo scraper genera un file JSON con la seguente struttura:

```json
{
  "url": "https://federicocalo.dev",
  "scraped_at": "2026-01-03T14:30:00.000000",
  "about": "Testo della sezione biografica...",
  "certifications": [
    {
      "title": "Nome certificazione",
      "organization": "Organizzazione emittente",
      "date": "Data conseguimento",
      "image_url": "URL immagine certificato"
    }
  ],
  "experience": [
    {
      "title": "Posizione lavorativa",
      "company": "Nome azienda",
      "period": "Periodo di lavoro",
      "description": "Descrizione del ruolo"
    }
  ],
  "education": [
    {
      "degree": "Titolo di studio",
      "institution": "Nome istituzione",
      "year": "Anno",
      "description": "Descrizione"
    }
  ],
  "skills": ["Python", "Java", "React", "..."],
  "contact": {
    "email": "email@example.com",
    "github": "https://github.com/...",
    "linkedin": "https://linkedin.com/in/...",
    "twitter": "https://twitter.com/...",
    "other_links": []
  }
}
```

## Funzionalità

- **Logging dettagliato**: Tracciamento completo delle operazioni di scraping
- **Gestione errori**: Robusta gestione delle eccezioni di rete
- **User-Agent personalizzato**: Per evitare blocchi da parte del server
- **Estrazione strutturata**: Dati organizzati in formato JSON
- **Deduplicazione**: Rimozione automatica di competenze duplicate

## Struttura del codice

- `FedericoCaloScraper`: Classe principale per il web scraping
  - `fetch_page()`: Recupero e parsing delle pagine web
  - `extract_certifications()`: Estrazione delle certificazioni
  - `extract_experience()`: Estrazione dell'esperienza lavorativa
  - `extract_education()`: Estrazione del percorso educativo
  - `extract_skills()`: Estrazione delle competenze tecniche
  - `extract_contact_info()`: Estrazione dei contatti
  - `extract_about()`: Estrazione della biografia
  - `scrape_all()`: Orchestrazione completa dello scraping
  - `save_to_json()`: Salvataggio dei dati in formato JSON

## Note

- Lo scraper è progettato per essere rispettoso del server
- Utilizza un timeout di 10 secondi per le richieste HTTP
- Il parsing è basato su classi CSS comuni nei portfolio web

## Licenza

Questo progetto è fornito a scopo educativo e di analisi.
