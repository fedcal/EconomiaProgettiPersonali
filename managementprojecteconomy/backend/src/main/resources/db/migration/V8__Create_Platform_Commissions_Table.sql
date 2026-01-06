-- ===================================
-- V8: Create Platform Commissions Table
-- ===================================
-- Tabella configurazione commissioni piattaforme booking
-- ===================================

CREATE TABLE platform_commissions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    platform_name VARCHAR(100) NOT NULL UNIQUE,
    commission_rate DECIMAL(5,2) NOT NULL COMMENT 'Percentuale (es. 15.00 per 15%)',
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_platform (platform_name),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserimento dati iniziali commissioni
INSERT INTO platform_commissions (platform_name, commission_rate, is_active, notes) VALUES
    ('Direct', 0.00, TRUE, 'Prenotazioni dirette senza commissioni'),
    ('Booking.com', 15.00, TRUE, 'Commissione standard Booking.com'),
    ('Airbnb', 14.00, TRUE, 'Commissione host Airbnb (media 14%)'),
    ('VRBO', 12.00, TRUE, 'Commissione VRBO/HomeAway'),
    ('Homeaway', 12.00, TRUE, 'Commissione HomeAway (ora VRBO)'),
    ('TripAdvisor', 13.00, TRUE, 'Commissione TripAdvisor Rentals');
