# 🚀 Quick Start Guide

Guida rapida per avviare il **Management Project Economy System** in locale.

## ⚡ Setup Rapido (5 minuti)

### 1. Prerequisiti

Verifica di avere installato:

```bash
java --version        # Java 21+
node --version        # Node.js 18+
npm --version         # npm 9+
mysql --version       # MySQL 8.x
python3 --version     # Python 3.8+
```

### 2. Database Setup

```bash
# Avvia MySQL
mysql -u root -p

# Crea database
CREATE DATABASE management_economy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 3. Configurazione Environment

Modifica il file `.env` nella root del progetto:

```bash
# managementprojecteconomy/.env
DB_URL=jdbc:mysql://localhost:3306/management_economy?useSSL=false&serverTimezone=Europe/Rome
DB_USERNAME=root
DB_PASSWORD=tua_password_mysql
BACKEND_PORT=8083
FRONTEND_PORT=4203
```

### 4. Avvio Backend (Terminal 1)

```bash
cd managementprojecteconomy/backend

# Compila e avvia
./mvnw spring-boot:run
```

✅ **Verifica**: Apri http://localhost:8083/api/v1/projects

Dovresti vedere: `[]` (array vuoto - nessun progetto ancora)

### 5. Migrazione Dati (Terminal 2 - Opzionale)

```bash
cd managementprojecteconomy/migration

# Setup Python venv
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure: venv\Scripts\activate  # Windows

# Installa dipendenze
pip install -r requirements.txt

# Esegui migrazione
python3 migrate_data.py
```

✅ **Verifica**: Ricarica http://localhost:8083/api/v1/projects

Dovresti vedere 3 progetti: FedericoCalo, CasaDelleMagnolie, PlayTheEvent

### 6. Avvio Frontend (Terminal 3)

```bash
cd managementprojecteconomy/frontend

# Installa dipendenze (solo la prima volta)
npm install

# Avvia dev server
npm start
```

✅ **Verifica**: Apri http://localhost:4203

Dovresti vedere la Dashboard con i 3 progetti (se hai eseguito la migrazione)

---

## 🎯 URL del Sistema

| Componente | URL | Descrizione |
|------------|-----|-------------|
| **Frontend** | http://localhost:4203 | Dashboard Angular |
| **Backend API** | http://localhost:8083/api/v1 | REST API Spring Boot |
| **Database** | localhost:3306/management_economy | MySQL |

---

## 📋 Comandi Utili

### Backend

```bash
cd backend

# Compila
./mvnw clean compile

# Esegui test
./mvnw test

# Package JAR
./mvnw clean package

# Avvia applicazione
./mvnw spring-boot:run

# Avvia su porta personalizzata
SERVER_PORT=8084 ./mvnw spring-boot:run
```

### Frontend

```bash
cd frontend

# Installa dipendenze
npm install

# Dev server (porta 4203)
npm start

# Build production
npm run build

# Test
npm test

# Lint
npm run lint
```

### Migration

```bash
cd migration

# Attiva virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt

# Esegui migrazione
python3 migrate_data.py

# Disattiva venv
deactivate
```

---

## 🧪 Test delle API

### Con curl

```bash
# Lista progetti
curl http://localhost:8083/api/v1/projects

# Crea progetto
curl -X POST http://localhost:8083/api/v1/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "code": "TEST",
    "type": "FREELANCE",
    "startDate": "2026-01-01",
    "status": "ACTIVE"
  }'

# Bookings per progetto
curl http://localhost:8083/api/v1/bookings/project/1

# Costi progetto
curl http://localhost:8083/api/v1/costs/one-time/project/1

# MRR subscriptions
curl http://localhost:8083/api/v1/subscriptions/project/3/mrr
```

### Con Browser

Apri http://localhost:8083/api/v1/projects nel browser

---

## 🐛 Troubleshooting

### Backend non si avvia

**Problema**: `Port 8083 already in use`

**Soluzione**:
```bash
# Trova processo sulla porta 8083
lsof -i :8083  # Linux/Mac
netstat -ano | findstr :8083  # Windows

# Killa il processo o cambia porta
SERVER_PORT=8084 ./mvnw spring-boot:run
```

**Problema**: `Failed to configure a DataSource`

**Soluzione**:
- Verifica che MySQL sia in esecuzione
- Controlla credenziali in `.env`
- Verifica che il database `management_economy` esista

### Frontend non si connette al Backend

**Problema**: `Failed to load resource: net::ERR_CONNECTION_REFUSED`

**Soluzione**:
1. Verifica che il backend sia in esecuzione: `curl http://localhost:8083/api/v1/projects`
2. Controlla la console browser per errori CORS
3. Verifica `environment.ts` abbia `apiUrl: 'http://localhost:8083/api/v1'`

### Migrazione dati fallisce

**Problema**: `mysql.connector.errors.ProgrammingError: 1146 Table doesn't exist`

**Soluzione**:
- Avvia prima il backend per far eseguire Flyway migrations
- Flyway crea automaticamente tutte le tabelle al primo avvio

---

## 📊 Struttura Database Dopo Migrazione

```sql
-- Verifica tabelle create
USE management_economy;
SHOW TABLES;

-- Output atteso:
-- +--------------------------------+
-- | Tables_in_management_economy   |
-- +--------------------------------+
-- | analytics_data                 |
-- | bookings                       |
-- | calculated_metrics             |
-- | flyway_schema_history          |
-- | one_time_costs                 |
-- | platform_commissions           |
-- | projects                       |
-- | recurring_costs                |
-- | revenue_streams                |
-- | subscriptions                  |
-- +--------------------------------+

-- Verifica progetti migrati
SELECT id, name, code, type FROM projects;

-- Verifica bookings
SELECT COUNT(*) FROM bookings;

-- Verifica costi
SELECT COUNT(*) FROM one_time_costs;
SELECT COUNT(*) FROM recurring_costs;
```

---

## 🔄 Workflow di Sviluppo

### Modifica Backend

1. Modifica codice Java in `backend/src/main/java/`
2. Spring Boot auto-reload (devtools)
3. Oppure riavvia: `Ctrl+C` e `./mvnw spring-boot:run`

### Modifica Frontend

1. Modifica codice in `frontend/src/app/`
2. Angular auto-reload automatico
3. Browser si aggiorna automaticamente

### Aggiungere nuovo Endpoint Backend

1. Crea metodo in `Controller`
2. Implementa logica in `Service`
3. Aggiungi query in `Repository` se necessario
4. Testa con curl o Postman

### Aggiungere nuovo Component Frontend

```bash
cd frontend

# Genera component
ng generate component features/my-component --standalone

# Aggiungi route in app.routes.ts
# Importa in parent component se necessario
```

---

## 💾 Backup e Restore Database

### Backup

```bash
mysqldump -u root -p management_economy > backup_$(date +%Y%m%d).sql
```

### Restore

```bash
mysql -u root -p management_economy < backup_20260103.sql
```

---

## 🚀 Deploy in Produzione

### Backend (JAR)

```bash
cd backend
./mvnw clean package -DskipTests

# JAR generato in: target/management-economy-1.0.0.jar

# Esegui in produzione
java -jar target/management-economy-1.0.0.jar \
  --spring.datasource.url=jdbc:mysql://prod-server:3306/management_economy \
  --spring.datasource.username=prod_user \
  --spring.datasource.password=prod_password \
  --server.port=8080
```

### Frontend (Static Files)

```bash
cd frontend
npm run build

# Files generati in: dist/management-economy-frontend/browser/
# Deploy su Nginx, Apache, o hosting statico

# Esempio Nginx config:
# location / {
#   root /var/www/management-economy;
#   try_files $uri $uri/ /index.html;
# }
```

---

## 📞 Supporto

- **Repository**: `/media/federicocalo/D/prj/EconomiaProgettiPersonali/managementprojecteconomy/`
- **README Completo**: `README.md`
- **Documentazione Backend**: `backend/README.md`
- **Documentazione Frontend**: `frontend/README.md`
- **Migration Guide**: `migration/README.md`

---

**Versione**: 1.0.0
**Ultimo Aggiornamento**: Gennaio 2026
**Autore**: Federico Calò
