package dev.federicocalo.managementeconomy.dto.request;

import dev.federicocalo.managementeconomy.enums.PaymentStatus;
import dev.federicocalo.managementeconomy.enums.RevenueType;
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
public class RevenueStreamRequest {

    @NotNull(message = "Il project ID è obbligatorio")
    private Long projectId;

    @NotBlank(message = "Il nome del ricavo è obbligatorio")
    @Size(max = 255)
    private String name;

    @NotNull(message = "L'importo è obbligatorio")
    @DecimalMin(value = "0.01", message = "L'importo deve essere maggiore di 0")
    private BigDecimal amount;

    @NotNull(message = "La data del ricavo è obbligatoria")
    @PastOrPresent(message = "La data del ricavo non può essere futura")
    private LocalDate revenueDate;

    @Size(max = 255)
    private String source;

    @NotNull(message = "Il tipo di ricavo è obbligatorio")
    private RevenueType revenueType;

    @Size(max = 5000)
    private String description;

    @Size(max = 100)
    private String invoiceNumber;

    private PaymentStatus paymentStatus;
}
