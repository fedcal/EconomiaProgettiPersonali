package dev.federicocalo.managementeconomy.enums;

/**
 * Stati di pagamento
 */
public enum PaymentStatus {
    /**
     * In attesa
     */
    PENDING,

    /**
     * Pagato (per costi)
     */
    PAID,

    /**
     * Ricevuto (per ricavi)
     */
    RECEIVED,

    /**
     * Annullato
     */
    CANCELLED
}
