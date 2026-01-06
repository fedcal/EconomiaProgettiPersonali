package dev.federicocalo.managementeconomy.enums;

/**
 * Tipologie di metriche KPI
 */
public enum MetricType {
    /**
     * Return on Investment - ((Revenue - Costs) / Costs) * 100
     */
    ROI,

    /**
     * Profitto - Revenue - Costs
     */
    PROFIT,

    /**
     * Tasso di occupazione (vacation rental) - (Nights Booked / Total Nights) * 100
     */
    OCCUPANCY_RATE,

    /**
     * Average Daily Rate (vacation rental) - Total Revenue / Total Nights
     */
    ADR,

    /**
     * Revenue Per Available Room (vacation rental) - Total Revenue / Total Available Nights
     */
    REVPAR,

    /**
     * Monthly Recurring Revenue (SaaS) - Ricavi ricorrenti mensili
     */
    MRR,

    /**
     * Annual Recurring Revenue (SaaS) - MRR * 12
     */
    ARR,

    /**
     * Churn Rate (SaaS) - Tasso di abbandono
     */
    CHURN_RATE,

    /**
     * Customer Acquisition Cost (SaaS) - Costo per acquisire un cliente
     */
    CAC,

    /**
     * Customer Lifetime Value (SaaS) - Valore lifetime del cliente
     */
    LTV
}
