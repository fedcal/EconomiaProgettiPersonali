package dev.federicocalo.managementeconomy.dto.response;

import dev.federicocalo.managementeconomy.enums.BillingCycle;
import dev.federicocalo.managementeconomy.enums.SubscriptionStatus;
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
public class SubscriptionResponse {

    private Long id;
    private Long projectId;
    private String projectName;
    private String customerName;
    private String customerEmail;
    private String planName;
    private BigDecimal mrr;
    private LocalDate startDate;
    private LocalDate endDate;
    private SubscriptionStatus subscriptionStatus;
    private BillingCycle billingCycle;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
