-- ===================================
-- V7: Create Calculated Metrics Table
-- ===================================
-- Tabella per metriche KPI calcolate
-- ===================================

CREATE TABLE calculated_metrics (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    metric_date DATE NOT NULL,
    metric_type VARCHAR(100) NOT NULL COMMENT 'ROI, PROFIT, OCCUPANCY_RATE, ADR, REVPAR, MRR, CHURN_RATE, CAC, LTV',
    metric_value DECIMAL(15,2) NOT NULL,
    period_type VARCHAR(50) DEFAULT 'MONTHLY' COMMENT 'DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY',
    calculation_method TEXT COMMENT 'Descrizione formula usata',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE KEY unique_project_metric_date (project_id, metric_type, metric_date),
    INDEX idx_type (metric_type),
    INDEX idx_project_date (project_id, metric_date),
    INDEX idx_period (period_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
