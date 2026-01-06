# Casa delle Magnolie Scraper

Web scraper per estrarre informazioni dal sito di affitto vacanze Casa delle Magnolie (https://casadellemagnolie.com).

## Descrizione

Questo scraper estrae informazioni strutturate sul property vacation rental, inclusi:

- **Informazioni proprietà**: Nome, slogan, posizione, capacità
- **Servizi e amenities**: Aria condizionata, parcheggio, cucina, WiFi, ecc.
- **Distanze**: Distanza dalla spiaggia e altri punti di interesse
- **Contatti**: Email, telefono, link social
- **Immagini**: Gallery fotografica della proprietà
- **Navigazione**: Pagine disponibili sul sito
- **Lingue**: Opzioni multilingua disponibili

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
python casadellemagnolie_scraper.py
```

I dati estratti verranno salvati in `casadellemagnolie_data.json`.

## Output

Lo scraper genera un file JSON con la seguente struttura:

```json
{
  "url": "https://casadellemagnolie.com",
  "scraped_at": "2026-01-03T14:30:00.000000",
  "property": {
    "name": "Casa delle Magnolie",
    "tagline": "Salento Lu sule, lu mare e lu ientu",
    "location": "Baia Verde, Gallipoli",
    "capacity": "9 beds",
    "description": "Descrizione della proprietà..."
  },
  "amenities": [
    {
      "name": "Aria Condizionata",
      "description": "Descrizione del servizio",
      "icon": "icon-class"
    }
  ],
  "distances": {
    "beach": "200 m",
    "city center": "2 km"
  },
  "contact": {
    "phone": "+39...",
    "email": "info@example.com",
    "website": "https://casadellemagnolie.com",
    "social_links": []
  },
  "images": [
    {
      "url": "https://casadellemagnolie.com/image.jpg",
      "alt": "Descrizione immagine",
      "title": "Titolo immagine"
    }
  ],
  "navigation": [
    {
      "text": "Home",
      "url": "https://casadellemagnolie.com/"
    }
  ],
  "languages": [
    {
      "name": "IT",
      "code": "it"
    }
  ]
}
```

## Funzionalità

- **Logging dettagliato**: Tracciamento completo delle operazioni di scraping
- **Gestione errori**: Robusta gestione delle eccezioni di rete
- **User-Agent personalizzato**: Per evitare blocchi da parte del server
- **Estrazione pattern**: Riconoscimento automatico di distanze, telefoni ed email
- **URL normalizzazione**: Conversione automatica di URL relativi in assoluti
- **Regex intelligente**: Estrazione di informazioni strutturate dal testo

## Struttura del codice

- `CasaDelleMagnolieScraper`: Classe principale per il web scraping
  - `fetch_page()`: Recupero e parsing delle pagine web
  - `extract_property_info()`: Estrazione informazioni base della proprietà
  - `extract_amenities()`: Estrazione servizi e comfort
  - `extract_distances()`: Estrazione distanze dai punti di interesse
  - `extract_contact_info()`: Estrazione contatti (email, telefono, social)
  - `extract_images()`: Estrazione gallery immagini
  - `extract_navigation()`: Estrazione menu di navigazione
  - `extract_languages()`: Estrazione lingue disponibili
  - `scrape_all()`: Orchestrazione completa dello scraping
  - `save_to_json()`: Salvataggio dei dati in formato JSON

## Note

- Lo scraper è progettato per essere rispettoso del server
- Utilizza un timeout di 10 secondi per le richieste HTTP
- Supporta il riconoscimento di pattern multilingua (italiano/inglese)
- Estrae automaticamente distanze, telefoni ed email anche se non strutturati

## Licenza

Questo progetto è fornito a scopo educativo e di analisi.
