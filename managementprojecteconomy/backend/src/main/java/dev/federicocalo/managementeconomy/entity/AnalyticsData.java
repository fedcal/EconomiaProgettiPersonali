package dev.federicocalo.managementeconomy.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Entity per Google Analytics data
 */
@Entity
@Table(name = "analytics_data", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"project_id", "report_date", "device_type", "traffic_source"})
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AnalyticsData {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    @Column(name = "report_date", nullable = false)
    private LocalDate reportDate;

    @Column(nullable = false)
    private Integer users;

    @Column(nullable = false)
    private Integer sessions;

    @Column(nullable = false)
    private Integer pageviews;

    @Column(name = "bounce_rate", precision = 5, scale = 2)
    private BigDecimal bounceRate;

    @Column(name = "device_type", length = 50)
    private String deviceType;

    @Column(name = "traffic_source", length = 255)
    private String trafficSource;

    private Integer conversions;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @Override
    public String toString() {
        return "AnalyticsData{" +
                "id=" + id +
                ", reportDate=" + reportDate +
                ", users=" + users +
                ", sessions=" + sessions +
                ", pageviews=" + pageviews +
                '}';
    }
}
