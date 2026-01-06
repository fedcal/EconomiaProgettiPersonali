package dev.federicocalo.managementeconomy.entity;

import dev.federicocalo.managementeconomy.enums.PaymentStatus;
import dev.federicocalo.managementeconomy.enums.RevenueType;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Entity per revenue streams (flussi di ricavo)
 */
@Entity
@Table(name = "revenue_streams")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RevenueStream {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, precision = 12, scale = 2)
    private BigDecimal amount;

    @Column(name = "revenue_date", nullable = false)
    private LocalDate revenueDate;

    @Column(length = 255)
    private String source;

    @Enumerated(EnumType.STRING)
    @Column(name = "revenue_type", nullable = false, length = 100)
    private RevenueType revenueType;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(name = "invoice_number", length = 100)
    private String invoiceNumber;

    @Enumerated(EnumType.STRING)
    @Column(name = "payment_status", length = 50)
    private PaymentStatus paymentStatus = PaymentStatus.RECEIVED;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Override
    public String toString() {
        return "RevenueStream{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", amount=" + amount +
                ", revenueType=" + revenueType +
                ", revenueDate=" + revenueDate +
                '}';
    }
}
