# 🚀 Deployment Guide

Guida completa per il deploy in produzione del **Management Project Economy System**.

## 📋 Indice

1. [Prerequisiti Produzione](#prerequisiti-produzione)
2. [Deploy Backend (Spring Boot)](#deploy-backend-spring-boot)
3. [Deploy Frontend (Angular)](#deploy-frontend-angular)
4. [Deploy Database (MySQL)](#deploy-database-mysql)
5. [Configurazione Reverse Proxy (Nginx)](#configurazione-reverse-proxy-nginx)
6. [SSL/HTTPS Setup](#sslhttps-setup)
7. [Monitoring e Logging](#monitoring-e-logging)
8. [Backup e Recovery](#backup-e-recovery)

---

## Prerequisiti Produzione

### Server Requirements

**Backend Server:**
- Ubuntu 22.04 LTS o superiore
- Java 21 JRE
- 2GB RAM minimo (4GB raccomandato)
- 20GB storage

**Frontend Server:**
- Nginx o Apache
- 1GB RAM
- 10GB storage

**Database Server:**
- MySQL 8.x
- 4GB RAM minimo
- 50GB storage
- Backup automatici configurati

---

## Deploy Backend (Spring Boot)

### 1. Build JAR di Produzione

```bash
cd backend

# Build production JAR
./mvnw clean package -DskipTests

# JAR generato in: target/management-economy-1.0.0.jar
```

### 2. Configurazione Produzione

Crea file `application-prod.properties`:

```properties
# Server
server.port=8080
server.compression.enabled=true

# Database (PRODUZIONE)
spring.datasource.url=jdbc:mysql://prod-db-server:3306/management_economy?useSSL=true&serverTimezone=UTC
spring.datasource.username=${DB_USERNAME}
spring.datasource.password=${DB_PASSWORD}

# JPA
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.format_sql=false

# Flyway
spring.flyway.enabled=true
spring.flyway.baseline-on-migrate=true

# Logging
logging.level.root=INFO
logging.level.dev.federicocalo.managementeconomy=INFO
logging.file.name=/var/log/management-economy/application.log

# CORS (aggiorna con dominio reale)
cors.origins=https://yourdomain.com
```

### 3. Systemd Service

Crea `/etc/systemd/system/management-economy.service`:

```ini
[Unit]
Description=Management Project Economy Backend
After=syslog.target network.target

[Service]
User=app
Group=app
WorkingDirectory=/opt/management-economy
ExecStart=/usr/bin/java -jar \
    -Dspring.profiles.active=prod \
    -Xmx1024m \
    -Xms512m \
    /opt/management-economy/management-economy-1.0.0.jar

SuccessExitStatus=143
StandardOutput=journal
StandardError=journal
Restart=always
RestartSec=10

Environment="DB_USERNAME=prod_user"
Environment="DB_PASSWORD=secure_password_here"

[Install]
WantedBy=multi-user.target
```

### 4. Deploy Steps

```bash
# 1. Crea utente app
sudo useradd -m -s /bin/bash app

# 2. Crea directory
sudo mkdir -p /opt/management-economy
sudo mkdir -p /var/log/management-economy

# 3. Copia JAR
sudo cp target/management-economy-1.0.0.jar /opt/management-economy/

# 4. Set permissions
sudo chown -R app:app /opt/management-economy
sudo chown -R app:app /var/log/management-economy

# 5. Enable service
sudo systemctl daemon-reload
sudo systemctl enable management-economy
sudo systemctl start management-economy

# 6. Verifica status
sudo systemctl status management-economy

# 7. Check logs
sudo journalctl -u management-economy -f
```

### 5. Health Check

```bash
# Test API
curl http://localhost:8080/api/v1/projects

# Expected: JSON array (progetti)
```

---

## Deploy Frontend (Angular)

### 1. Build Produzione

```bash
cd frontend

# Build con optimizations
npm run build -- --configuration production

# Output in: dist/management-economy-frontend/browser/
```

### 2. Deploy su Nginx

#### a) Installa Nginx

```bash
sudo apt update
sudo apt install nginx -y
```

#### b) Crea Nginx Config

File `/etc/nginx/sites-available/management-economy`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    root /var/www/management-economy;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Angular routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy (opzionale se stesso server)
    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### c) Deploy Files

```bash
# Crea directory
sudo mkdir -p /var/www/management-economy

# Copia build
sudo cp -r dist/management-economy-frontend/browser/* /var/www/management-economy/

# Set permissions
sudo chown -R www-data:www-data /var/www/management-economy

# Enable site
sudo ln -s /etc/nginx/sites-available/management-economy /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

#### d) Verifica

```bash
curl http://yourdomain.com
# Dovrebbe restituire l'HTML dell'app
```

---

## Deploy Database (MySQL)

### 1. Setup MySQL Produzione

```bash
# Installa MySQL
sudo apt install mysql-server -y

# Secure installation
sudo mysql_secure_installation
```

### 2. Crea Database e Utente

```sql
-- Login come root
sudo mysql

-- Crea database
CREATE DATABASE management_economy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crea utente produzione
CREATE USER 'prod_user'@'localhost' IDENTIFIED BY 'secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON management_economy.* TO 'prod_user'@'localhost';
FLUSH PRIVILEGES;

-- Verifica
SHOW DATABASES;
SELECT user, host FROM mysql.user WHERE user = 'prod_user';
```

### 3. Configurazione MySQL

File `/etc/mysql/mysql.conf.d/mysqld.cnf`:

```ini
[mysqld]
# Character set
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# Performance
max_connections = 200
innodb_buffer_pool_size = 1G

# Logging
log_error = /var/log/mysql/error.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2

# Binary logging per replica
server-id = 1
log_bin = /var/log/mysql/mysql-bin.log
binlog_expire_logs_seconds = 604800
```

Restart MySQL:
```bash
sudo systemctl restart mysql
```

### 4. Migrazione Iniziale

Al primo deploy, Flyway creerà automaticamente le tabelle quando il backend si avvia.

```bash
# Verifica tabelle create
mysql -u prod_user -p management_economy

mysql> SHOW TABLES;
# Dovrebbe mostrare 10 tabelle + flyway_schema_history
```

---

## Configurazione Reverse Proxy (Nginx)

### Setup Completo con SSL

```nginx
# HTTP → HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    root /var/www/management-economy;
    index index.html;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## SSL/HTTPS Setup

### Let's Encrypt (Certbot)

```bash
# Installa Certbot
sudo apt install certbot python3-certbot-nginx -y

# Ottieni certificato
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (già configurato da certbot)
sudo systemctl status certbot.timer

# Test renewal
sudo certbot renew --dry-run
```

---

## Monitoring e Logging

### 1. Backend Logs

```bash
# Journalctl
sudo journalctl -u management-economy -f

# Log file
tail -f /var/log/management-economy/application.log

# Grep errors
grep -i error /var/log/management-economy/application.log
```

### 2. Nginx Logs

```bash
# Access log
tail -f /var/log/nginx/access.log

# Error log
tail -f /var/log/nginx/error.log
```

### 3. MySQL Logs

```bash
# Error log
tail -f /var/log/mysql/error.log

# Slow queries
tail -f /var/log/mysql/slow.log
```

### 4. Health Monitoring (Optional)

Installa monitoring tool:

```bash
# Prometheus + Grafana
# o
# Uptime Kuma (simple dashboard)

docker run -d --restart=always \
  -p 3001:3001 \
  -v uptime-kuma:/app/data \
  --name uptime-kuma \
  louislam/uptime-kuma:1

# Access: http://localhost:3001
# Add monitor: http://yourdomain.com/api/v1/projects
```

---

## Backup e Recovery

### 1. Database Backup Script

File `/opt/scripts/backup-db.sh`:

```bash
#!/bin/bash

# Config
DB_NAME="management_economy"
DB_USER="prod_user"
DB_PASS="secure_password_here"
BACKUP_DIR="/backups/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/backup_${DATE}.sql.gz

# Delete old backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completato: backup_${DATE}.sql.gz"
```

### 2. Cron Job Backup

```bash
# Edit crontab
sudo crontab -e

# Backup giornaliero alle 2:00 AM
0 2 * * * /opt/scripts/backup-db.sh >> /var/log/backup.log 2>&1
```

### 3. Restore da Backup

```bash
# Decompress
gunzip backup_20260103_020000.sql.gz

# Restore
mysql -u prod_user -p management_economy < backup_20260103_020000.sql
```

### 4. Application Files Backup

```bash
# Backup JAR e configs
tar -czf /backups/app/backend_$(date +%Y%m%d).tar.gz \
  /opt/management-economy

# Backup frontend
tar -czf /backups/app/frontend_$(date +%Y%m%d).tar.gz \
  /var/www/management-economy
```

---

## Checklist Pre-Deploy

### Backend
- [ ] Build JAR con `-DskipTests`
- [ ] Configurato `application-prod.properties`
- [ ] Variabili ambiente sicure (DB_PASSWORD)
- [ ] Systemd service creato
- [ ] Health check funzionante
- [ ] Logging configurato

### Frontend
- [ ] Build production con optimization
- [ ] Environment config aggiornato (API URL produzione)
- [ ] Nginx config testato (`nginx -t`)
- [ ] Static files copiati
- [ ] Gzip compression abilitata

### Database
- [ ] MySQL installato e secured
- [ ] Database creato con charset utf8mb4
- [ ] Utente produzione con privileges limitati
- [ ] Backup automatici configurati
- [ ] Slow query log abilitato

### SSL/Security
- [ ] Certificato SSL installato (Let's Encrypt)
- [ ] HTTPS redirect configurato
- [ ] Security headers aggiunti
- [ ] Firewall configurato (ufw)
- [ ] SSH key-based auth only

### Monitoring
- [ ] Logs rotati (logrotate)
- [ ] Health checks configurati
- [ ] Alert email/SMS setup (opzionale)
- [ ] Uptime monitoring (opzionale)

---

## Firewall Setup (UFW)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow MySQL (solo da backend server se separato)
# sudo ufw allow from BACKEND_IP to any port 3306

# Status
sudo ufw status
```

---

## Post-Deploy Verification

### 1. Backend API

```bash
# Health check
curl https://yourdomain.com/api/v1/projects

# Expected: JSON array
```

### 2. Frontend

```bash
# Home page
curl https://yourdomain.com

# Expected: HTML con Angular app
```

### 3. Database

```bash
# Verifica connessione backend→DB
sudo journalctl -u management-economy | grep "HikariPool"

# Expected: "HikariPool-1 - Start completed"
```

### 4. SSL

```bash
# Test SSL
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Expected: Certificate chain, TLS 1.2/1.3
```

---

## Troubleshooting Produzione

### Backend non risponde

```bash
# Check service
sudo systemctl status management-economy

# Check logs
sudo journalctl -u management-economy -n 100

# Check port
sudo lsof -i :8080

# Restart
sudo systemctl restart management-economy
```

### Database connection failed

```bash
# Check MySQL running
sudo systemctl status mysql

# Test connection
mysql -u prod_user -p management_economy

# Check grants
mysql> SHOW GRANTS FOR 'prod_user'@'localhost';
```

### Nginx 502 Bad Gateway

```bash
# Check backend running
curl http://localhost:8080/api/v1/projects

# Check Nginx config
sudo nginx -t

# Check Nginx logs
tail -f /var/log/nginx/error.log
```

---

## 🎯 Production URLs Structure

```
Frontend:  https://yourdomain.com
Backend:   https://yourdomain.com/api/v1/*
Database:  localhost:3306 (interno, non esposto)
```

---

**Ultimo Aggiornamento**: Gennaio 2026
**Versione**: 1.0.0
**Autore**: Federico Calò
