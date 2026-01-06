-- ===================================
-- V6: Create Analytics Data Table
-- ===================================
-- Tabella per dati Google Analytics
-- ===================================

CREATE TABLE analytics_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    report_date DATE NOT NULL,
    users INT DEFAULT 0,
    sessions INT DEFAULT 0,
    pageviews INT DEFAULT 0,
    bounce_rate DECIMAL(5,2),
    avg_session_duration INT COMMENT 'Secondi',
    device_type VARCHAR(50) COMMENT 'Desktop, Mobile, Tablet',
    traffic_source VARCHAR(100) COMMENT 'Organic, Direct, Social, Referral',
    top_page VARCHAR(500),
    conversions INT DEFAULT 0,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    UNIQUE KEY unique_project_date_device (project_id, report_date, device_type, traffic_source),
    INDEX idx_project_date (project_id, report_date),
    INDEX idx_device (device_type),
    INDEX idx_source (traffic_source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
