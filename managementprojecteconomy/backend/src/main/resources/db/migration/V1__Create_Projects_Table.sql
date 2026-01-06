-- ===================================
-- V1: Create Projects Table
-- ===================================
-- Tabella principale per i progetti gestiti
-- ===================================

CREATE TABLE projects (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    code VARCHAR(50) NOT NULL UNIQUE COMMENT 'FEDERICOCALO, CASADELLEMAGNOLIE, PLAYTHEEVENT',
    type VARCHAR(100) NOT NULL COMMENT 'FREELANCE, VACATION_RENTAL, SAAS',
    description TEXT,
    start_date DATE NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    status VARCHAR(50) DEFAULT 'ACTIVE' COMMENT 'ACTIVE, ARCHIVED, SUSPENDED',
    target_occupancy_rate DECIMAL(5,2) COMMENT 'Solo per VACATION_RENTAL (es. 60.00)',
    target_monthly_revenue DECIMAL(12,2),
    target_roi DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_code (code),
    INDEX idx_status (status),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
