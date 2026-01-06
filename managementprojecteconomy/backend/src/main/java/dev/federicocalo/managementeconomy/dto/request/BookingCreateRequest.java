package dev.federicocalo.managementeconomy.dto.request;

import jakarta.validation.constraints.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * DTO per creazione nuova prenotazione
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BookingCreateRequest {

    @NotNull(message = "Il project ID è obbligatorio")
    private Long projectId;

    @NotNull(message = "La data di check-in è obbligatoria")
    @FutureOrPresent(message = "La data di check-in non può essere nel passato")
    private LocalDate checkinDate;

    @NotNull(message = "La data di check-out è obbligatoria")
    @Future(message = "La data di check-out deve essere futura")
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

    @Size(max = 255, message = "Il nome dell'ospite non può superare i 255 caratteri")
    private String guestName;

    @Email(message = "Email non valida")
    @Size(max = 255, message = "L'email non può superare i 255 caratteri")
    private String guestEmail;

    @Size(max = 50, message = "Il telefono non può superare i 50 caratteri")
    private String guestPhone;

    @Size(max = 5000, message = "Le note non possono superare i 5000 caratteri")
    private String notes;

    /**
     * Validazione personalizzata: checkout deve essere dopo checkin
     */
    @AssertTrue(message = "La data di check-out deve essere successiva alla data di check-in")
    public boolean isCheckoutAfterCheckin() {
        if (checkinDate == null || checkoutDate == null) {
            return true; // Lascia che @NotNull gestisca i null
        }
        return checkoutDate.isAfter(checkinDate);
    }
}
