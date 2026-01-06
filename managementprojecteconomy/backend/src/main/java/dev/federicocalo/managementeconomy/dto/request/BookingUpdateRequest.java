package dev.federicocalo.managementeconomy.dto.request;

import dev.federicocalo.managementeconomy.enums.BookingStatus;
import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO per aggiornamento prenotazione esistente
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BookingUpdateRequest {

    @NotNull(message = "La data di check-in è obbligatoria")
    private LocalDate checkinDate;

    @NotNull(message = "La data di check-out è obbligatoria")
    private LocalDate checkoutDate;

    @NotNull(message = "Il numero di ospiti è obbligatorio")
    @Min(value = 1, message = "Deve esserci almeno 1 ospite")
    @Max(value = 50, message = "Il numero massimo di ospiti è 50")
    private Integer guests;

    @NotNull(message = "Il prezzo è obbligatorio")
    @DecimalMin(value = "0.01", message = "Il prezzo deve essere maggiore di 0")
    private BigDecimal price;

    @NotBlank(message = "La piattaforma è obbligatoria")
    @Size(max = 100, message = "La piattaforma non può superare i 100 caratteri")
    private String platform;

    private BookingStatus bookingStatus;

    @Size(max = 255, message = "Il nome dell'ospite non può superare i 255 caratteri")
    private String guestName;

    @Email(message = "Email non valida")
    @Size(max = 255, message = "L'email non può superare i 255 caratteri")
    private String guestEmail;

    @Size(max = 50, message = "Il telefono non può superare i 50 caratteri")
    private String guestPhone;

    @Size(max = 5000, message = "Le note non possono superare i 5000 caratteri")
    private String notes;

    @AssertTrue(message = "La data di check-out deve essere successiva alla data di check-in")
    public boolean isCheckoutAfterCheckin() {
        if (checkinDate == null || checkoutDate == null) {
            return true;
        }
        return checkoutDate.isAfter(checkinDate);
    }
}
