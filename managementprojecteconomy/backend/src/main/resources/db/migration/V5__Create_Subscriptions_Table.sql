-- ===================================
-- V5: Create Subscriptions Table
-- ===================================
-- Tabella per subscriptions SaaS (PlayTheEvent)
-- ===================================

CREATE TABLE subscriptions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255),
    plan_name VARCHAR(100) NOT NULL COMMENT 'Basic, Pro, Enterprise',
    mrr DECIMAL(12,2) NOT NULL COMMENT 'Monthly Recurring Revenue',
    start_date DATE NOT NULL,
    end_date DATE COMMENT 'NULL se attiva',
    subscription_status VARCHAR(50) DEFAULT 'ACTIVE' COMMENT 'ACTIVE, CANCELLED, EXPIRED, TRIAL',
    payment_method VARCHAR(100),
    billing_cycle VARCHAR(50) DEFAULT 'MONTHLY' COMMENT 'MONTHLY, YEARLY',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_status (project_id, subscription_status),
    INDEX idx_status (subscription_status),
    INDEX idx_plan (plan_name),
    INDEX idx_dates (start_date, end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
