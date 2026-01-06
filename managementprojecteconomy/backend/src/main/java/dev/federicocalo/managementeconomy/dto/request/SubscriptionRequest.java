package dev.federicocalo.managementeconomy.dto.request;

import dev.federicocalo.managementeconomy.enums.BillingCycle;
import dev.federicocalo.managementeconomy.enums.SubscriptionStatus;
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
public class SubscriptionRequest {

    @NotNull(message = "Il project ID è obbligatorio")
    private Long projectId;

    @NotBlank(message = "Il nome del cliente è obbligatorio")
    @Size(max = 255)
    private String customerName;

    @Email(message = "Email non valida")
    @Size(max = 255)
    private String customerEmail;

    @NotBlank(message = "Il nome del piano è obbligatorio")
    @Size(max = 100)
    private String planName;

    @NotNull(message = "L'MRR è obbligatorio")
    @DecimalMin(value = "0.01", message = "L'MRR deve essere maggiore di 0")
    private BigDecimal mrr;

    @NotNull(message = "La data di inizio è obbligatoria")
    private LocalDate startDate;

    private LocalDate endDate;

    @NotNull(message = "Lo stato della subscription è obbligatorio")
    private SubscriptionStatus subscriptionStatus;

    @NotNull(message = "Il ciclo di fatturazione è obbligatorio")
    private BillingCycle billingCycle;

    @AssertTrue(message = "La data di fine deve essere successiva alla data di inizio")
    public boolean isEndDateValid() {
        if (endDate == null) {
            return true;
        }
        return endDate.isAfter(startDate);
    }
}
