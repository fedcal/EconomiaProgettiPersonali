package dev.federicocalo.managementeconomy.dto.response;

import dev.federicocalo.managementeconomy.enums.BookingStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * DTO di risposta per prenotazione
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BookingResponse {

    private Long id;
    private Long projectId;
    private String projectName;
    private LocalDate checkinDate;
    private LocalDate checkoutDate;
    private Integer guests;
    private Integer nights;
    private BigDecimal price;
    private BigDecimal pricePerNight;
    private String platform;
    private BigDecimal commissionRate;
    private BigDecimal commissionAmount;
    private BigDecimal netRevenue;
    private BookingStatus bookingStatus;
    private String guestName;
    private String guestEmail;
    private String guestPhone;
    private String notes;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
