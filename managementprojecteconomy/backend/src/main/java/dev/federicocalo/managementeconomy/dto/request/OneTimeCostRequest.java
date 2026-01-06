package dev.federicocalo.managementeconomy.dto.request;

import dev.federicocalo.managementeconomy.enums.CostCategory;
import dev.federicocalo.managementeconomy.enums.PaymentStatus;
import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OneTimeCostRequest {

    @NotNull(message = "Il project ID è obbligatorio")
    private Long projectId;

    @NotBlank(message = "Il nome del costo è obbligatorio")
    @Size(max = 255)
    private String name;

    @NotNull(message = "L'importo è obbligatorio")
    @DecimalMin(value = "0.01", message = "L'importo deve essere maggiore di 0")
    private BigDecimal amount;

    @NotNull(message = "La data del costo è obbligatoria")
    @PastOrPresent(message = "La data del costo non può essere futura")
    private LocalDate costDate;

    @NotNull(message = "La categoria è obbligatoria")
    private CostCategory category;

    @Size(max = 5000)
    private String description;

    @Size(max = 100)
    private String invoiceNumber;

    @Size(max = 255)
    private String supplier;

    private PaymentStatus paymentStatus;
}
