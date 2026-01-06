-- ===================================
-- V3: Create Revenue Streams Table
-- ===================================
-- Tabella per ricavi generici
-- ===================================

CREATE TABLE revenue_streams (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    revenue_date DATE NOT NULL,
    source VARCHAR(255) COMMENT 'Direct Client, Udemy, Affiliate, Booking.com, Airbnb, etc.',
    revenue_type VARCHAR(100) NOT NULL COMMENT 'consultation, project, course, passive, booking, subscription',
    description TEXT,
    invoice_number VARCHAR(100),
    payment_status VARCHAR(50) DEFAULT 'RECEIVED' COMMENT 'PENDING, RECEIVED, CANCELLED',
    client_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    INDEX idx_project_date (project_id, revenue_date),
    INDEX idx_type (revenue_type),
    INDEX idx_source (source),
    INDEX idx_payment_status (payment_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
