# GitHub Configuration

## Descrizione del Progetto

Questo progetto contiene:
- **Web Scraping Analysis**: Analisi dei dati da web scraping per vari progetti
- **Management Project Economy**: Applicazione full-stack (Java backend + Angular frontend) per la gestione economica dei progetti
- **Documentazione**: Guide su Agile, Project Management, Financial Management, Leadership e Productivity

## Branch Protection Rules

Applica le seguenti regole al branch `master`:

1. ✅ Require pull request reviews before merging (almeno 1 reviewer)
2. ✅ Require status checks to pass before merging
3. ✅ Require branches to be up to date before merging
4. ✅ Include administrators in restrictions

## Impostazioni di Sicurezza

- ✅ Enable Secret scanning
- ✅ Enable Dependabot alerts
- ✅ Enable Dependabot security updates
- ✅ Enable private vulnerability reporting

## Workflow Automation

Sono configurati i seguenti workflow:
- **Python Tests**: Testa il codice Python su 3.9, 3.10, 3.11
- **Java Build**: Compila e testa il backend con Maven
- **Angular Build**: Compila e testa il frontend Angular

## Code Owners

Il file `CODEOWNERS` definisce automaticamente i reviewer per i PR.

## Dependabot Configuration

Dependabot aggiorna automaticamente le dipendenze settimanalmente per:
- Python (pip)
- Maven (Java)
- npm (Node.js)
