package dev.federicocalo.managementeconomy.entity;

import dev.federicocalo.managementeconomy.enums.ProjectStatus;
import dev.federicocalo.managementeconomy.enums.ProjectType;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Entity per i progetti gestiti dal sistema
 */
@Entity
@Table(name = "projects")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Project {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    @Column(nullable = false, unique = true, length = 50)
    private String code;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 100)
    private ProjectType type;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(name = "start_date", nullable = false)
    private LocalDate startDate;

    @Column(length = 3)
    private String currency = "EUR";

    @Enumerated(EnumType.STRING)
    @Column(length = 50)
    private ProjectStatus status = ProjectStatus.ACTIVE;

    @Column(name = "target_occupancy_rate", precision = 5, scale = 2)
    private BigDecimal targetOccupancyRate;

    @Column(name = "target_monthly_revenue", precision = 12, scale = 2)
    private BigDecimal targetMonthlyRevenue;

    @Column(name = "target_roi", precision = 5, scale = 2)
    private BigDecimal targetRoi;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // Relationships - Lazy loading per performance
    // Note: Le relazioni saranno completate quando creeremo le altre entities

    @Override
    public String toString() {
        return "Project{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", code='" + code + '\'' +
                ", type=" + type +
                ", status=" + status +
                '}';
    }
}
