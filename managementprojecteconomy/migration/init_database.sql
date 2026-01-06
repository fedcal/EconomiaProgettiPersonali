-- ===================================
-- MANAGEMENT PROJECT ECONOMY
-- Inizializzazione Database
-- ===================================

-- Crea database se non esiste
CREATE DATABASE IF NOT EXISTS management_economy
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Usa il database
USE management_economy;

-- Verifica creazione
SELECT 'Database management_economy creato con successo!' AS status;
SHOW TABLES;
