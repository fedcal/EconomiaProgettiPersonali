package dev.federicocalo.managementeconomy.dto.response;

import dev.federicocalo.managementeconomy.enums.PaymentStatus;
import dev.federicocalo.managementeconomy.enums.RevenueType;
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
public class RevenueStreamResponse {

    private Long id;
    private Long projectId;
    private String projectName;
    private String name;
    private BigDecimal amount;
    private LocalDate revenueDate;
    private String source;
    private RevenueType revenueType;
    private String description;
    private String invoiceNumber;
    private PaymentStatus paymentStatus;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
