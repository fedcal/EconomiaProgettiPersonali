package dev.federicocalo.managementeconomy.dto.request;

import dev.federicocalo.managementeconomy.enums.CostCategory;
import dev.federicocalo.managementeconomy.enums.Frequency;
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
public class RecurringCostRequest {

    @NotNull(message = "Il project ID è obbligatorio")
    private Long projectId;

    @NotBlank(message = "Il nome del costo è obbligatorio")
    @Size(max = 255)
    private String name;

    @NotNull(message = "L'importo è obbligatorio")
    @DecimalMin(value = "0.01", message = "L'importo deve essere maggiore di 0")
    private BigDecimal amount;

    @NotNull(message = "La frequenza è obbligatoria")
    private Frequency frequency;

    @NotNull(message = "La categoria è obbligatoria")
    private CostCategory category;

    @NotNull(message = "La data di inizio è obbligatoria")
    private LocalDate startDate;

    private LocalDate endDate;

    @Size(max = 5000)
    private String description;

    private Boolean isActive = true;

    private Boolean autoRenew = true;

    @AssertTrue(message = "La data di fine deve essere successiva alla data di inizio")
    public boolean isEndDateValid() {
        if (endDate == null) {
            return true;
        }
        return endDate.isAfter(startDate);
    }
}
