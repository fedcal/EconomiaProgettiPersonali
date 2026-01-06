package dev.federicocalo.managementeconomy.entity;

import dev.federicocalo.managementeconomy.enums.CostCategory;
import dev.federicocalo.managementeconomy.enums.PaymentStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Entity per costi una tantum
 */
@Entity
@Table(name = "one_time_costs")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class OneTimeCost {

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

    @Column(name = "cost_date", nullable = false)
    private LocalDate costDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 100)
    private CostCategory category;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(name = "invoice_number", length = 100)
    private String invoiceNumber;

    @Column(length = 255)
    private String supplier;

    @Enumerated(EnumType.STRING)
    @Column(name = "payment_status", length = 50)
    private PaymentStatus paymentStatus = PaymentStatus.PAID;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Override
    public String toString() {
        return "OneTimeCost{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", amount=" + amount +
                ", category=" + category +
                ", costDate=" + costDate +
                '}';
    }
}
