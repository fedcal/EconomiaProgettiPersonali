# Management Project Economy

Sistema completo di gestione economica multi-progetto per monitorare ricavi, costi e KPI di tre progetti web.

## 📊 Progetti Gestiti

1. **FedericoCalo.dev** - Portfolio professionale e servizi freelance
2. **CasaDelleMagnolie.com** - Property vacation rental in Salento
3. **PlayTheEvent.com** - Piattaforma SaaS per gestione eventi

## 🏗️ Architettura

### Monorepo Structure

```
managementprojecteconomy/
├── backend/          # Spring Boot 3.4 + Java 21
├── frontend/         # Angular 19 + TypeScript
├── migration/        # Python data migration scripts
└── .env             # Environment configuration (tracked in git - dev only)
```

## 🚀 Backend (Spring Boot)

### Stack Tecnologico

- **Spring Boot**: 3.4.1
- **Java**: 21
- **Database**: MySQL 8.x
- **ORM**: Hibernate + Spring Data JPA
- **Migrations**: Flyway
- **DTO Mapping**: MapStruct
- **Boilerplate Reduction**: Lombok
- **Validation**: Jakarta Validation (JSR-303)

### Moduli Implementati

#### Core Modules
- ✅ **PROJECTS** - Gestione progetti con 12 REST endpoints
- ✅ **BOOKINGS** - Prenotazioni vacation rental (auto-calcolo commissioni)
- ✅ **COSTS** - Costi una tantum e ricorrenti (17 endpoints)
- ✅ **REVENUES** - Flussi di ricavo (11 endpoints)
- ✅ **SUBSCRIPTIONS** - Gestione subscriptions SaaS con MRR tracking
- ✅ **ANALYTICS** - Storage dati Google Analytics
- ✅ **CALCULATED_METRICS** - Storage metriche KPI pre-calcolate
- ✅ **PLATFORM_COMMISSIONS** - Configurazione commissioni piattaforme booking

#### Business Logic Services
- ✅ **MetricsCalculationService** - Calcolo KPI:
  - **Generali**: ROI, Profit, Total Costs/Revenue, Growth Rates
  - **Vacation Rental**: ADR, Occupancy Rate, RevPAR, Commissioni
  - **SaaS**: MRR, ARR, ARPU, Active Subscriptions

### Database Schema

8 migration Flyway scripts creano:
- **10 tabelle** principali
- **11 enum** types
- **40+ query custom** per analytics e aggregazioni
- **Constraints** e relazioni FK/UK

### API Endpoints

- **67+ REST endpoints** totali
- Base URL: `http://localhost:8083/api/v1`
- CORS abilitato per `http://localhost:4203`

#### Endpoint Examples

```
GET    /api/v1/projects
POST   /api/v1/projects
GET    /api/v1/bookings/project/{projectId}
POST   /api/v1/bookings
GET    /api/v1/costs/one-time/project/{projectId}/total?startDate=...&endDate=...
GET    /api/v1/revenues/project/{projectId}/monthly
GET    /api/v1/subscriptions/project/{projectId}/mrr
```

### Configurazione

#### application.properties

```properties
server.port=8083
spring.datasource.url=${DB_URL}
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}
spring.jpa.hibernate.ddl-auto=validate
```

#### .env (Development)

```bash
DB_URL=jdbc:mysql://localhost:3306/management_economy?useSSL=false&serverTimezone=Europe/Rome
DB_USERNAME=root
DB_PASSWORD=your_password
BACKEND_PORT=8083
FRONTEND_PORT=4203
CORS_ORIGINS=http://localhost:4203
```

### Build & Run

```bash
cd backend

# Compile
./mvnw clean compile

# Run tests
./mvnw test

# Package
./mvnw clean package

# Run application
./mvnw spring-boot:run
```

## 🎨 Frontend (Angular 19)

### Stack Tecnologico

- **Angular**: 19 (standalone components)
- **TypeScript**: Latest
- **Styling**: SCSS + Angular Material
- **Charts**: Chart.js
- **HTTP**: HttpClient with RxJS

### Struttura

```
frontend/src/app/
├── core/
│   ├── models/          # TypeScript interfaces (DTOs)
│   │   ├── enums.ts
│   │   ├── project.model.ts
│   │   ├── booking.model.ts
│   │   ├── cost.model.ts
│   │   └── revenue.model.ts
│   └── services/        # HTTP services
│       ├── project.service.ts
│       └── booking.service.ts
└── environments/
    └── environment.ts   # API URL configuration
```

### Models

- ✅ **11 Enums** (mirror backend Java enums)
- ✅ **TypeScript interfaces** per tutte le entities
- ✅ **Request/Response DTOs**

### Services

- ✅ **ProjectService** - CRUD + status management
- ✅ **BookingService** - Bookings + KPI calculation endpoints
- Pattern ready per: CostService, RevenueService, SubscriptionService

### Configuration

**environment.ts**
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8083/api/v1'
};
```

**angular.json** - porta 4203
```json
{
  "serve": {
    "options": {
      "port": 4203
    }
  }
}
```

### Build & Run

```bash
cd frontend

# Install dependencies
npm install

# Development server (port 4203)
npm start

# Build for production
npm run build
```

## 🔄 Migration (Python)

Script Python per migrare dati esistenti da JSON a MySQL.

### Files

- `migrate_data.py` - Script principale (300+ lines)
- `requirements.txt` - Dipendenze Python
- `README.md` - Istruzioni d'uso

### Features

- ✅ Legge JSON da tre progetti esistenti
- ✅ Inserisce dati in MySQL (idempotent)
- ✅ Auto-calcola commissioni booking
- ✅ Mapping categorie e enums
- ✅ Error handling robusto

### Usage

```bash
cd migration
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python3 migrate_data.py
```

## 📦 Setup Completo del Progetto

### Prerequisiti

- Java 21+
- Node.js 18+ & npm
- MySQL 8.x
- Python 3.8+
- Maven 3.8+

### Step-by-Step Setup

#### 1. Database

```bash
mysql -u root -p
CREATE DATABASE management_economy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 2. Environment

Crea/modifica `.env` nella root:

```bash
DB_URL=jdbc:mysql://localhost:3306/management_economy?useSSL=false&serverTimezone=Europe/Rome
DB_USERNAME=root
DB_PASSWORD=your_mysql_password
BACKEND_PORT=8083
FRONTEND_PORT=4203
```

#### 3. Backend

```bash
cd backend
./mvnw clean install
./mvnw spring-boot:run
# Flyway migrations eseguite automaticamente
```

Verifica: http://localhost:8083/api/v1/projects

#### 4. Migration (Opzionale)

```bash
cd migration
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 migrate_data.py
```

#### 5. Frontend

```bash
cd frontend
npm install
npm start
```

Accedi a: http://localhost:4203

## 📊 Metriche e KPI Disponibili

### Generali (Tutti i Progetti)
- **ROI** (Return on Investment) - `(Revenue - Costs) / Costs * 100`
- **Profit** - `Revenue - Costs`
- **Total Costs** - Somma costi una tantum + ricorrenti
- **Total Revenue** - Somma flussi ricavo
- **Growth Rate** - Crescita % tra periodi

### Vacation Rental (CasaDelleMagnolie)
- **ADR** (Average Daily Rate) - `Total Revenue / Total Nights`
- **Occupancy Rate** - `(Nights Booked / Available Nights) * 100`
- **RevPAR** (Revenue Per Available Room) - `Total Revenue / Total Available Nights`
- **Commissioni Totali** - Auto-calcolate per piattaforma
- **Net Revenue** - `Gross Revenue - Commissioni`

### SaaS (PlayTheEvent)
- **MRR** (Monthly Recurring Revenue) - Somma subscriptions attive
- **ARR** (Annual Recurring Revenue) - `MRR * 12`
- **ARPU** (Average Revenue Per User) - `MRR / Active Subscriptions`
- **Active Subscriptions Count**

## 🗂️ Database Schema Overview

### Tabelle Principali

| Tabella | Descrizione | Righe Attese |
|---------|-------------|--------------|
| `projects` | Progetti gestiti | 3 |
| `one_time_costs` | Costi una tantum | 50+ |
| `recurring_costs` | Costi ricorrenti | 20+ |
| `revenue_streams` | Flussi di ricavo | 100+ |
| `bookings` | Prenotazioni vacation rental | 200+ |
| `subscriptions` | Subscriptions SaaS | 10+ |
| `platform_commissions` | Config commissioni | 4 |
| `analytics_data` | Dati Google Analytics | 1000+ |
| `calculated_metrics` | KPI pre-calcolati | 500+ |

## 🔐 Sicurezza

- ✅ Validation layer (backend + frontend)
- ✅ Global Exception Handler
- ✅ CORS configurato
- ⚠️ **NOTA**: `.env` è tracciato in git per sviluppo. Per produzione, usare variabili d'ambiente del server.

## 📈 Statistiche del Progetto

### Backend
- **67 Java source files** compilati
- **67+ REST API endpoints**
- **10 Entities** con JPA
- **10 Repositories** con 40+ custom queries
- **5 Services** con business logic
- **6 Controllers**

### Frontend
- **11 Enums TypeScript**
- **5+ Model interfaces**
- **2+ HTTP Services** (pattern completo)
- **Angular 19** standalone components

### Migration
- **1 Python script** (300+ lines)
- **Support per 3 progetti**
- **Auto-calcolo** commissioni e metriche

## 🚦 Prossimi Passi

### Backend
- [ ] Avvio e test Spring Boot + Flyway
- [ ] Verifica creazione tabelle MySQL
- [ ] Test API con Postman/Insomnia

### Frontend
- [ ] Completare componenti UI
- [ ] Dashboard con Chart.js
- [ ] Forms per CRUD operations
- [ ] Integrazione Angular Material

### Integration
- [ ] Eseguire migrazione dati
- [ ] Test end-to-end completo
- [ ] Performance testing

## 📝 Licenza

Proprietario: Federico Calò
Uso: Personale - Gestione progetti privati

## 🤝 Contributi

Progetto privato - non accetta contributi esterni.

---

**Versione**: 1.0.0
**Data**: Gennaio 2026
**Autore**: Federico Calò
**Stack**: Spring Boot 3.4 + Angular 19 + MySQL 8
