package dev.federicocalo.managementeconomy.entity;

import dev.federicocalo.managementeconomy.enums.MetricType;
import dev.federicocalo.managementeconomy.enums.PeriodType;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Entity per metriche KPI calcolate
 */
@Entity
@Table(name = "calculated_metrics", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"project_id", "metric_date", "metric_type", "period_type"})
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CalculatedMetric {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    @Column(name = "metric_date", nullable = false)
    private LocalDate metricDate;

    @Enumerated(EnumType.STRING)
    @Column(name = "metric_type", nullable = false, length = 100)
    private MetricType metricType;

    @Column(name = "metric_value", nullable = false, precision = 15, scale = 2)
    private BigDecimal metricValue;

    @Enumerated(EnumType.STRING)
    @Column(name = "period_type", nullable = false, length = 50)
    private PeriodType periodType;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Override
    public String toString() {
        return "CalculatedMetric{" +
                "id=" + id +
                ", metricType=" + metricType +
                ", metricValue=" + metricValue +
                ", metricDate=" + metricDate +
                ", periodType=" + periodType +
                '}';
    }
}
