package dev.federicocalo.managementeconomy.entity;

import dev.federicocalo.managementeconomy.enums.BookingStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

/**
 * Entity per prenotazioni vacation rental
 */
@Entity
@Table(name = "bookings")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Booking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    // Nota: revenue_stream_id sarà aggiunto quando creeremo RevenueStream entity

    @Column(name = "checkin_date", nullable = false)
    private LocalDate checkinDate;

    @Column(name = "checkout_date", nullable = false)
    private LocalDate checkoutDate;

    @Column(nullable = false)
    private Integer guests;

    @Column(nullable = false)
    private Integer nights;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal price;

    @Column(name = "price_per_night", nullable = false, precision = 12, scale = 2)
    private BigDecimal pricePerNight;

    @Column(nullable = false, length = 100)
    private String platform;

    @Column(name = "commission_rate", precision = 5, scale = 2)
    private BigDecimal commissionRate;

    @Column(name = "commission_amount", precision = 12, scale = 2)
    private BigDecimal commissionAmount;

    @Column(name = "net_revenue", nullable = false, precision = 12, scale = 2)
    private BigDecimal netRevenue;

    @Enumerated(EnumType.STRING)
    @Column(name = "booking_status", length = 50)
    private BookingStatus bookingStatus = BookingStatus.CONFIRMED;

    @Column(name = "guest_name")
    private String guestName;

    @Column(name = "guest_email")
    private String guestEmail;

    @Column(name = "guest_phone", length = 50)
    private String guestPhone;

    @Column(columnDefinition = "TEXT")
    private String notes;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    /**
     * Calcola automaticamente campi derivati prima di persist/update
     */
    @PrePersist
    @PreUpdate
    public void calculateDerivedFields() {
        // Calcola nights
        if (checkinDate != null && checkoutDate != null) {
            this.nights = (int) ChronoUnit.DAYS.between(checkinDate, checkoutDate);
        }

        // Calcola price per night
        if (price != null && nights != null && nights > 0) {
            this.pricePerNight = price.divide(
                BigDecimal.valueOf(nights),
                2,
                java.math.RoundingMode.HALF_UP
            );
        }

        // Calcola net revenue
        if (price != null && commissionAmount != null) {
            this.netRevenue = price.subtract(commissionAmount);
        } else if (price != null) {
            this.netRevenue = price;
        }
    }

    @Override
    public String toString() {
        return "Booking{" +
                "id=" + id +
                ", platform='" + platform + '\'' +
                ", checkinDate=" + checkinDate +
                ", checkoutDate=" + checkoutDate +
                ", nights=" + nights +
                ", price=" + price +
                ", status=" + bookingStatus +
                '}';
    }
}
