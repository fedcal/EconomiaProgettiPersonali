-- ===================================
-- V2: Create Costs Tables
-- ===================================
-- Tabelle per costi una tantum e ricorrenti
-- ===================================

-- Tabella costi una tantum
CREATE TABLE one_time_costs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    cost_date DATE NOT NULL,
    category VARCHAR(100) NOT NULL COMMENT 'Infrastructure, Branding, Content, Development, Marketing, Property',
    description TEXT,
    invoice_number VARCHAR(100),
    supplier VARCHAR(255),
    payment_status VARCHAR(50) DEFAULT 'PAID' COMMENT 'PENDING, PAID, CANCELLED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_date (project_id, cost_date),
    INDEX idx_category (category),
    INDEX idx_payment_status (payment_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabella costi ricorrenti
CREATE TABLE recurring_costs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    frequency VARCHAR(50) NOT NULL COMMENT 'MONTHLY, QUARTERLY, YEARLY',
    category VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE COMMENT 'NULL se attivo',
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    auto_renew BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_active (project_id, is_active),
    INDEX idx_frequency (frequency),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
