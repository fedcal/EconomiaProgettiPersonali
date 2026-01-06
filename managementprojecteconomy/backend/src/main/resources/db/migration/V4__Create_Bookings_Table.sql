-- ===================================
-- V4: Create Bookings Table
-- ===================================
-- Tabella per prenotazioni vacation rental
-- ===================================

CREATE TABLE bookings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    project_id BIGINT NOT NULL,
    revenue_stream_id BIGINT COMMENT 'Link alla revenue generata',
    checkin_date DATE NOT NULL,
    checkout_date DATE NOT NULL,
    guests INT NOT NULL,
    nights INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    price_per_night DECIMAL(12,2) NOT NULL,
    platform VARCHAR(100) NOT NULL COMMENT 'Direct, Booking.com, Airbnb, VRBO, Homeaway, TripAdvisor',
    commission_rate DECIMAL(5,2) COMMENT 'Percentuale commissione (es. 15.00)',
    commission_amount DECIMAL(12,2) COMMENT 'Importo commissione',
    net_revenue DECIMAL(12,2) NOT NULL COMMENT 'price - commission_amount',
    booking_status VARCHAR(50) DEFAULT 'CONFIRMED' COMMENT 'PENDING, CONFIRMED, CANCELLED, COMPLETED',
    guest_name VARCHAR(255),
    guest_email VARCHAR(255),
    guest_phone VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (revenue_stream_id) REFERENCES revenue_streams(id) ON DELETE SET NULL,
    INDEX idx_project_checkin (project_id, checkin_date),
    INDEX idx_project_checkout (project_id, checkout_date),
    INDEX idx_platform (platform),
    INDEX idx_status (booking_status),
    INDEX idx_dates (checkin_date, checkout_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
