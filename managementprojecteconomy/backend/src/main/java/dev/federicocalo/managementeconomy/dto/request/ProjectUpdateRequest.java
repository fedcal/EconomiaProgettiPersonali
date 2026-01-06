package dev.federicocalo.managementeconomy.dto.request;

import dev.federicocalo.managementeconomy.enums.ProjectStatus;
import dev.federicocalo.managementeconomy.enums.ProjectType;
import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO per aggiornamento progetto esistente
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProjectUpdateRequest {

    @NotBlank(message = "Il nome del progetto è obbligatorio")
    @Size(min = 3, max = 255, message = "Il nome deve essere tra 3 e 255 caratteri")
    private String name;

    @NotNull(message = "Il tipo di progetto è obbligatorio")
    private ProjectType type;

    private ProjectStatus status;

    @Size(max = 5000, message = "La descrizione non può superare i 5000 caratteri")
    private String description;

    @NotNull(message = "La data di inizio è obbligatoria")
    private LocalDate startDate;

    @Size(min = 3, max = 3, message = "La valuta deve essere di 3 caratteri (es. EUR)")
    private String currency;

    @DecimalMin(value = "0.0", message = "Il target occupancy rate deve essere >= 0")
    @DecimalMax(value = "100.0", message = "Il target occupancy rate deve essere <= 100")
    private BigDecimal targetOccupancyRate;

    @DecimalMin(value = "0.0", message = "Il target monthly revenue deve essere >= 0")
    private BigDecimal targetMonthlyRevenue;

    @DecimalMin(value = "0.0", message = "Il target ROI deve essere >= 0")
    private BigDecimal targetRoi;
}
