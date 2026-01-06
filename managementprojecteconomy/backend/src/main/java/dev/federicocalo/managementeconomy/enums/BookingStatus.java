package dev.federicocalo.managementeconomy.enums;

/**
 * Stati di prenotazione (vacation rental)
 */
public enum BookingStatus {
    /**
     * In attesa di conferma
     */
    PENDING,

    /**
     * Confermata
     */
    CONFIRMED,

    /**
     * Annullata
     */
    CANCELLED,

    /**
     * Completata
     */
    COMPLETED
}
