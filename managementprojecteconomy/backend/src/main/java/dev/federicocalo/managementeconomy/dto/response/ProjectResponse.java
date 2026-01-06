package dev.federicocalo.managementeconomy.dto.response;

import dev.federicocalo.managementeconomy.enums.ProjectStatus;
import dev.federicocalo.managementeconomy.enums.ProjectType;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * DTO di risposta per progetto
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProjectResponse {

    private Long id;
    private String name;
    private String code;
    private ProjectType type;
    private String description;
    private LocalDate startDate;
    private String currency;
    private ProjectStatus status;
    private BigDecimal targetOccupancyRate;
    private BigDecimal targetMonthlyRevenue;
    private BigDecimal targetRoi;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
