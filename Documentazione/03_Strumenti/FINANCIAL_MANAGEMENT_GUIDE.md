# 💰 Guida alla Gestione Finanziaria dei Progetti

Sistema completo di **Project Management Finanziario** per gestire budget, costi, ricavi e ROI come un vero Project Manager.

---

## 📊 Panoramica Sistema

Ogni progetto ha ora un sistema di gestione finanziaria che include:

✅ **Tracking Costi** - One-time e ricorrenti
✅ **Tracking Ricavi** - Per fonte e tipo
✅ **Calcolo ROI** - Return on Investment automatico
✅ **Forecast** - Proiezioni a 6-12 mesi
✅ **Break-even Analysis** - Quando raggiungi il pareggio
✅ **Visualizzazioni** - 4 grafici finanziari automatici
✅ **Report Completi** - PDF/TXT con analisi dettagliata

---

## 🎯 Metriche Calcolate

### **Generali (Entrambi i Progetti)**
- **Profitto** = Ricavi - Costi
- **ROI** = (Profitto / Costi) × 100
- **Break-even** = Mesi necessari per pareggiare investimento
- **Forecast** = Proiezione ricavi/costi futuri

### **Specifiche Vacation Rental (CasaDelleMagnolie)**
- **Occupancy Rate** = (Settimane Prenotate / 52) × 100
- **ADR** (Average Daily Rate) = Ricavo Totale / Notti Totali
- **RevPAR** = Ricavo Totale / Settimane Disponibili
- **Commissioni Piattaforme** = Tracking automatico per Booking, Airbnb, etc.

---

## 🚀 Come Usare

### **1. Primo Utilizzo - Dati di Esempio**

```bash
# FedericoCalo
cd "Analisi Web Scraping progetti/FedericoCalo"
source venv/bin/activate
python3 financial_manager.py

# CasaDelleMagnolie
cd "../CasaDelleMagnolie"
source venv/bin/activate
python3 financial_manager.py
```

Il sistema genera:
- `financial_data.json` - Database finanziario
- `financial_report.txt` - Report completo
- `financial_*.png` - 4 grafici

---

### **2. Personalizzare con i Tuoi Dati**

Modifica il file `financial_data.json` o usa il codice Python:

#### **FedericoCalo.dev - Esempio**

```python
from financial_manager import FinancialManager

fm = FinancialManager("FedericoCalo.dev")

# Aggiungi costi una tantum
fm.add_one_time_cost("Dominio .dev", 36.00, "2025-01-15", "Infrastructure")
fm.add_one_time_cost("Logo Design", 150.00, "2025-01-20", "Branding")

# Aggiungi costi ricorrenti
fm.add_recurring_cost("Hosting VPS", 15.00, "monthly", "Infrastructure", "2025-01-01")
fm.add_recurring_cost("Google Workspace", 6.00, "monthly", "Tools", "2025-01-01")

# Aggiungi ricavi
fm.add_revenue_stream("Consulenza Cliente A", 1500.00, "2025-02-15", "Direct Client", "consultation")
fm.add_revenue_stream("Progetto Web", 3000.00, "2025-04-10", "Direct Client", "project")

# Salva e genera report
fm.save_to_json()
report = fm.generate_financial_report()
print(report)

# Crea grafici
fm.create_visualizations()
```

#### **CasaDelleMagnolie.com - Esempio**

```python
from financial_manager import VacationRentalFinancialManager

fm = VacationRentalFinancialManager("Casa delle Magnolie")

# Aggiungi costi proprietà
fm.add_one_time_cost("Foto professionali", 250.00, "2025-03-01", "Marketing")
fm.add_one_time_cost("Nuovi elettrodomestici", 800.00, "2025-02-20", "Property")

# Aggiungi costi operativi
fm.add_recurring_cost("Pulizie", 80.00, "monthly", "Operations", "2025-04-01")
fm.add_recurring_cost("Utenze", 120.00, "monthly", "Utilities", "2025-01-01")

# Aggiungi prenotazioni
fm.add_booking(
    checkin="2025-07-05",
    checkout="2025-07-12",
    guests=6,
    price=1200.00,
    platform="Booking.com"  # Calcola commissione automaticamente
)

fm.add_booking(
    checkin="2025-07-14",
    checkout="2025-07-21",
    guests=8,
    price=1400.00,
    platform="Direct"  # Nessuna commissione
)

# Salva e report
fm.save_to_json()
report = fm.generate_financial_report()
print(report)
```

---

## 📁 Struttura File JSON

### **FedericoCalo - financial_data.json**

```json
{
  "project_info": {
    "name": "FedericoCalo.dev",
    "type": "Professional Portfolio & Services",
    "start_date": "2025-01-01",
    "currency": "EUR"
  },
  "one_time_costs": [
    {
      "name": "Dominio .dev",
      "amount": 36.00,
      "date": "2025-01-15",
      "category": "Infrastructure"
    }
  ],
  "recurring_costs": [
    {
      "name": "Hosting VPS",
      "amount": 15.00,
      "frequency": "monthly",
      "category": "Infrastructure",
      "start_date": "2025-01-01"
    }
  ],
  "revenue_streams": [
    {
      "name": "Consulenza Cliente A",
      "amount": 1500.00,
      "date": "2025-02-15",
      "source": "Direct Client",
      "type": "consultation"
    }
  ]
}
```

### **CasaDelleMagnolie - financial_data.json**

Include anche sezione `bookings`:

```json
{
  "bookings": [
    {
      "checkin": "2025-07-05",
      "checkout": "2025-07-12",
      "guests": 6,
      "nights": 7,
      "price": 1200.00,
      "price_per_night": 171.43,
      "platform": "Booking.com",
      "commission": 180.00
    }
  ],
  "occupancy": {
    "total_weeks": 52,
    "booked_weeks": 9.9
  }
}
```

---

## 📊 Output Generati

### **1. Report Testuale** (`financial_report.txt`)

```
================================================================================
REPORT FINANZIARIO - FedericoCalo.dev
================================================================================

RIEPILOGO GENERALE
--------------------------------------------------------------------------------
Costi totali:    €465.00
Ricavi totali:   €5,870.00
Profitto:        €5,405.00
ROI:             1162.37%

BREAKDOWN COSTI PER CATEGORIA
...

PREVISIONE 6 MESI
...

ANALISI BREAK-EVEN
Mesi per raggiungere break-even: 1.5 mesi
Data prevista break-even: 2025-02-13
```

### **2. Grafici Automatici** (PNG)

1. **`financial_costs_vs_revenue.png`** - Confronto costi/ricavi/profitto
2. **`financial_cost_breakdown.png`** - Pie chart costi per categoria
3. **`financial_revenue_breakdown.png`** - Pie chart ricavi per tipo
4. **`financial_forecast.png`** - Forecast 12 mesi

---

## 💡 Casi d'Uso Pratici

### **Scenario 1: Pianificare un Nuovo Servizio**

```python
# Voglio offrire consulenze SEO
# Calcolo: vale la pena?

fm = FinancialManager()
fm.load_from_json()

# Aggiungo costo tool SEO
fm.add_recurring_cost("SEO Tool", 99.00, "monthly", "Tools", "2025-04-01")

# Stimo 2 consulenze/mese a €500
for month in range(1, 7):
    fm.add_revenue_stream(
        f"Consulenza SEO - Mese {month}",
        1000.00,  # 2 × €500
        f"2025-{month:02d}-15",
        "Direct",
        "consultation"
    )

# Calcolo ROI
roi = fm.calculate_roi()
print(f"ROI Servizio SEO: {roi}%")
# Se > 100% → vale la pena!
```

### **Scenario 2: Valutare Stagione CasaDelleMagnolie**

```python
fm = VacationRentalFinancialManager()
fm.load_from_json()

# Vedo quanto ho guadagnato in estate
summer_revenue = fm.calculate_total_revenue("2025-06-01", "2025-09-30")
summer_costs = fm.calculate_total_costs("2025-06-01", "2025-09-30")
summer_profit = summer_revenue - summer_costs

print(f"Estate 2025:")
print(f"  Ricavi: €{summer_revenue:,.2f}")
print(f"  Profitto: €{summer_profit:,.2f}")

# Occupancy rate estate
occupancy = fm.calculate_occupancy_rate()
print(f"  Occupazione: {occupancy}%")
```

### **Scenario 3: Decidere se Investire in Marketing**

```python
# Opzione: Spendere €500 in Ads
# Obiettivo: +3 prenotazioni @ €1000 ciascuna

fm = VacationRentalFinancialManager()
fm.add_one_time_cost("Google Ads Campaign", 500.00, "2025-05-01", "Marketing")

# Simulo ricavi attesi
for i in range(3):
    fm.add_booking("2025-06-15", "2025-06-22", 6, 1000.00, "Direct")

profit = fm.calculate_profit()
roi = fm.calculate_roi()

print(f"ROI Campagna: {roi}%")
# Se ROI > 200% → ottimo investimento!
```

---

## 🎯 Best Practices

### **1. Aggiorna Regolarmente**
- **Settimanale**: Aggiungi nuove spese/ricavi
- **Mensile**: Genera report e analizza trend
- **Trimestrale**: Rivedi forecast e obiettivi

### **2. Categorizza Correttamente**

**Categorie Costi FedericoCalo:**
- Infrastructure (hosting, domini)
- Tools (software, abbonamenti)
- Marketing (ads, SEO tools)
- Content (foto, video)
- Branding (logo, design)
- Development (template, plugins)

**Categorie Costi CasaDelleMagnolie:**
- Property (arredamento, elettrodomestici)
- Operations (pulizie, check-in)
- Utilities (acqua, luce, gas, wifi)
- Maintenance (riparazioni)
- Insurance (assicurazioni)
- Marketing (foto, ads, traduzioni)

### **3. Traccia Tutto**
Anche piccole spese contano:
- €10 dominio → Infrastructure
- €5 stock photo → Content
- €50 regalo cliente → Marketing

### **4. Usa Forecast per Pianificare**
```python
forecast = fm.generate_monthly_forecast(12)
# Usa per:
# - Budget annuale
# - Decisioni investimento
# - Cash flow planning
```

---

## 📈 KPI da Monitorare

### **FedericoCalo.dev**
- ✅ **ROI > 500%** - Obiettivo anno 1
- ✅ **Profitto mensile > €1000** - Sostenibilità
- ✅ **Break-even < 3 mesi** - Recupero veloce
- ✅ **Costi ricorrenti < 30% ricavi** - Margine sano

### **CasaDelleMagnolie.com**
- ✅ **Occupancy > 60%** - Target mercato
- ✅ **ADR > €150** - Prezzo competitivo
- ✅ **Commissioni < 20%** - Più prenotazioni dirette
- ✅ **Profitto netto > €10,000/anno** - Obiettivo minimo

---

## 🔄 Workflow Consigliato

### **Settimanale**
```bash
1. Aggiungi nuove spese/ricavi al JSON
2. Rigenera report: python3 financial_manager.py
3. Verifica KPI e confronta con settimana precedente
```

### **Mensile**
```bash
1. Backup financial_data.json (es. financial_data_2025-01.json)
2. Analizza trend mensile
3. Aggiorna forecast
4. Condividi grafici con stakeholder (se applicabile)
```

### **Trimestrale**
```bash
1. Review completa budget vs actual
2. Rivedi strategie se ROI < target
3. Pianifica investimenti prossimo trimestre
```

---

## 🛠️ Comandi Rapidi

```bash
# Generare report
python3 financial_manager.py

# Solo grafici
python3 -c "from financial_manager import *; fm = FinancialManager(); fm.load_from_json(); fm.create_visualizations()"

# Calcolo ROI rapido
python3 -c "from financial_manager import *; fm = FinancialManager(); fm.load_from_json(); print(f'ROI: {fm.calculate_roi()}%')"

# Export CSV (personalizza)
python3 -c "import json; import csv; data = json.load(open('financial_data.json')); ..."
```

---

## 💼 Pro Tips

1. **Versioning**: Salva copie mensili del JSON per storico
2. **Backup**: Commit su Git per non perdere dati
3. **Privacy**: Non committare dati sensibili su repo pubblici
4. **Automazione**: Cron job per report settimanali automatici
5. **Integration**: Collegabile a Google Sheets via API per dashboard condivise

---

## 📞 Supporto

Problemi o domande? Controlla:
- File di esempio già creati in ogni progetto
- Commenti nel codice Python
- Questa guida

---

**Ora hai il controllo finanziario completo dei tuoi progetti! 🎉**