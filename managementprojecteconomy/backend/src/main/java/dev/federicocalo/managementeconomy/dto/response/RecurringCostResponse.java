package dev.federicocalo.managementeconomy.dto.response;

import dev.federicocalo.managementeconomy.enums.CostCategory;
import dev.federicocalo.managementeconomy.enums.Frequency;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RecurringCostResponse {

    private Long id;
    private Long projectId;
    private String projectName;
    private String name;
    private BigDecimal amount;
    private Frequency frequency;
    private CostCategory category;
    private LocalDate startDate;
    private LocalDate endDate;
    private String description;
    private Boolean isActive;
    private Boolean autoRenew;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
