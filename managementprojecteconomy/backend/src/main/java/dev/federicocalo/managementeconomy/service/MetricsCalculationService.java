package dev.federicocalo.managementeconomy.service;

import dev.federicocalo.managementeconomy.repository.*;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.Year;
import java.time.temporal.ChronoUnit;

/**
 * Service per il calcolo delle metriche KPI
 * Implementa la business logic per tutti i calcoli finanziari e di performance
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional(readOnly = true)
public class MetricsCalculationService {

    private final OneTimeCostRepository oneTimeCostRepository;
    private final RecurringCostRepository recurringCostRepository;
    private final RevenueStreamRepository revenueStreamRepository;
    private final BookingRepository bookingRepository;
    private final SubscriptionRepository subscriptionRepository;

    // ========================== METRICHE GENERALI ==========================

    /**
     * Calcola i costi totali per un progetto in un range di date
     */
    public BigDecimal calculateTotalCosts(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating total costs for project {} between {} and {}", projectId, startDate, endDate);

        // Costi una tantum nel periodo
        BigDecimal oneTimeCosts = oneTimeCostRepository.calculateTotalByDateRange(projectId, startDate, endDate);

        // Costi ricorrenti mensili attivi * numero di mesi
        BigDecimal monthlyRecurringCosts = recurringCostRepository.calculateTotalMonthlyActive(projectId);
        long months = ChronoUnit.MONTHS.between(startDate, endDate) + 1;
        BigDecimal recurringCosts = monthlyRecurringCosts.multiply(BigDecimal.valueOf(months));

        BigDecimal totalCosts = oneTimeCosts.add(recurringCosts);
        log.debug("Total costs: {} (one-time: {}, recurring: {})", totalCosts, oneTimeCosts, recurringCosts);

        return totalCosts;
    }

    /**
     * Calcola i ricavi totali per un progetto in un range di date
     */
    public BigDecimal calculateTotalRevenue(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating total revenue for project {} between {} and {}", projectId, startDate, endDate);

        BigDecimal totalRevenue = revenueStreamRepository.calculateTotalByDateRange(projectId, startDate, endDate);
        log.debug("Total revenue: {}", totalRevenue);

        return totalRevenue;
    }

    /**
     * Calcola il profitto per un progetto in un range di date
     * Profit = Revenue - Costs
     */
    public BigDecimal calculateProfit(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating profit for project {} between {} and {}", projectId, startDate, endDate);

        BigDecimal revenue = calculateTotalRevenue(projectId, startDate, endDate);
        BigDecimal costs = calculateTotalCosts(projectId, startDate, endDate);
        BigDecimal profit = revenue.subtract(costs);

        log.debug("Profit: {} (revenue: {}, costs: {})", profit, revenue, costs);
        return profit;
    }

    /**
     * Calcola il ROI (Return on Investment) per un progetto
     * ROI = ((Revenue - Costs) / Costs) * 100
     */
    public BigDecimal calculateROI(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating ROI for project {} between {} and {}", projectId, startDate, endDate);

        BigDecimal costs = calculateTotalCosts(projectId, startDate, endDate);
        BigDecimal revenue = calculateTotalRevenue(projectId, startDate, endDate);

        if (costs.compareTo(BigDecimal.ZERO) == 0) {
            log.warn("Cannot calculate ROI: costs are zero");
            return BigDecimal.ZERO;
        }

        BigDecimal profit = revenue.subtract(costs);
        BigDecimal roi = profit.divide(costs, 4, RoundingMode.HALF_UP)
                .multiply(BigDecimal.valueOf(100));

        log.debug("ROI: {}% (profit: {}, costs: {})", roi, profit, costs);
        return roi;
    }

    // ========================== METRICHE VACATION RENTAL ==========================

    /**
     * Calcola ADR (Average Daily Rate) - Prezzo medio per notte
     * ADR = Total Revenue / Total Nights Sold
     */
    public BigDecimal calculateADR(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating ADR for project {} between {} and {}", projectId, startDate, endDate);

        BigDecimal totalRevenue = bookingRepository.calculateTotalRevenueByDateRange(projectId, startDate, endDate);
        Integer totalNights = bookingRepository.calculateTotalNightsByDateRange(projectId, startDate, endDate);

        if (totalNights == null || totalNights == 0) {
            log.warn("Cannot calculate ADR: no nights sold");
            return BigDecimal.ZERO;
        }

        BigDecimal adr = totalRevenue.divide(BigDecimal.valueOf(totalNights), 2, RoundingMode.HALF_UP);
        log.debug("ADR: {} (revenue: {}, nights: {})", adr, totalRevenue, totalNights);

        return adr;
    }

    /**
     * Calcola ADR per anno
     */
    public BigDecimal calculateADRByYear(Long projectId, int year) {
        LocalDate startDate = LocalDate.of(year, 1, 1);
        LocalDate endDate = LocalDate.of(year, 12, 31);
        return calculateADR(projectId, startDate, endDate);
    }

    /**
     * Calcola Occupancy Rate (Tasso di occupazione)
     * Occupancy Rate = (Nights Booked / Total Available Nights) * 100
     */
    public BigDecimal calculateOccupancyRate(Long projectId, int year) {
        log.debug("Calculating occupancy rate for project {} in year {}", projectId, year);

        Integer totalNights = bookingRepository.calculateTotalNightsByYear(projectId, year);
        int daysInYear = Year.of(year).length();

        if (totalNights == null) {
            totalNights = 0;
        }

        BigDecimal occupancyRate = BigDecimal.valueOf(totalNights)
                .divide(BigDecimal.valueOf(daysInYear), 4, RoundingMode.HALF_UP)
                .multiply(BigDecimal.valueOf(100));

        log.debug("Occupancy rate: {}% (nights booked: {}, days in year: {})",
                occupancyRate, totalNights, daysInYear);

        return occupancyRate;
    }

    /**
     * Calcola RevPAR (Revenue Per Available Room)
     * RevPAR = Total Revenue / Total Available Nights
     * oppure RevPAR = ADR * Occupancy Rate
     */
    public BigDecimal calculateRevPAR(Long projectId, int year) {
        log.debug("Calculating RevPAR for project {} in year {}", projectId, year);

        LocalDate startDate = LocalDate.of(year, 1, 1);
        LocalDate endDate = LocalDate.of(year, 12, 31);

        BigDecimal totalRevenue = bookingRepository.calculateTotalRevenueByDateRange(projectId, startDate, endDate);
        int daysInYear = Year.of(year).length();

        BigDecimal revpar = totalRevenue.divide(BigDecimal.valueOf(daysInYear), 2, RoundingMode.HALF_UP);
        log.debug("RevPAR: {} (revenue: {}, days: {})", revpar, totalRevenue, daysInYear);

        return revpar;
    }

    /**
     * Calcola commissioni totali pagate alle piattaforme
     */
    public BigDecimal calculateTotalCommissions(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating total commissions for project {} between {} and {}",
                projectId, startDate, endDate);

        BigDecimal totalCommissions = bookingRepository.calculateTotalCommissionsByDateRange(
                projectId, startDate, endDate);

        log.debug("Total commissions: {}", totalCommissions);
        return totalCommissions;
    }

    /**
     * Calcola ricavo netto (revenue - commissioni) per vacation rental
     */
    public BigDecimal calculateNetRevenue(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating net revenue for project {} between {} and {}",
                projectId, startDate, endDate);

        BigDecimal totalRevenue = bookingRepository.calculateTotalRevenueByDateRange(projectId, startDate, endDate);
        BigDecimal totalCommissions = bookingRepository.calculateTotalCommissionsByDateRange(
                projectId, startDate, endDate);

        BigDecimal netRevenue = totalRevenue.subtract(totalCommissions);
        log.debug("Net revenue: {} (revenue: {}, commissions: {})",
                netRevenue, totalRevenue, totalCommissions);

        return netRevenue;
    }

    // ========================== METRICHE SAAS ==========================

    /**
     * Calcola MRR (Monthly Recurring Revenue) totale
     * Somma di tutti gli MRR delle subscriptions attive
     */
    public BigDecimal calculateMRR(Long projectId) {
        log.debug("Calculating MRR for project: {}", projectId);

        BigDecimal mrr = subscriptionRepository.calculateTotalMRR(projectId);
        log.debug("Total MRR: {}", mrr);

        return mrr;
    }

    /**
     * Calcola ARR (Annual Recurring Revenue)
     * ARR = MRR * 12
     */
    public BigDecimal calculateARR(Long projectId) {
        log.debug("Calculating ARR for project: {}", projectId);

        BigDecimal mrr = calculateMRR(projectId);
        BigDecimal arr = mrr.multiply(BigDecimal.valueOf(12));

        log.debug("ARR: {} (MRR: {})", arr, mrr);
        return arr;
    }

    /**
     * Conta subscriptions attive
     */
    public long countActiveSubscriptions(Long projectId) {
        log.debug("Counting active subscriptions for project: {}", projectId);

        long count = subscriptionRepository.countActiveSubscriptions(projectId);
        log.debug("Active subscriptions: {}", count);

        return count;
    }

    /**
     * Calcola ARPU (Average Revenue Per User)
     * ARPU = MRR / Active Subscriptions
     */
    public BigDecimal calculateARPU(Long projectId) {
        log.debug("Calculating ARPU for project: {}", projectId);

        BigDecimal mrr = calculateMRR(projectId);
        long activeSubscriptions = countActiveSubscriptions(projectId);

        if (activeSubscriptions == 0) {
            log.warn("Cannot calculate ARPU: no active subscriptions");
            return BigDecimal.ZERO;
        }

        BigDecimal arpu = mrr.divide(BigDecimal.valueOf(activeSubscriptions), 2, RoundingMode.HALF_UP);
        log.debug("ARPU: {} (MRR: {}, active subs: {})", arpu, mrr, activeSubscriptions);

        return arpu;
    }

    // ========================== METRICHE COMPARATIVE ==========================

    /**
     * Confronta due periodi e calcola il % di crescita
     */
    public BigDecimal calculateGrowthRate(BigDecimal currentValue, BigDecimal previousValue) {
        if (previousValue.compareTo(BigDecimal.ZERO) == 0) {
            return BigDecimal.ZERO;
        }

        BigDecimal difference = currentValue.subtract(previousValue);
        return difference.divide(previousValue, 4, RoundingMode.HALF_UP)
                .multiply(BigDecimal.valueOf(100));
    }

    /**
     * Calcola la crescita del profitto tra due periodi
     */
    public BigDecimal calculateProfitGrowth(Long projectId,
                                             LocalDate currentStart, LocalDate currentEnd,
                                             LocalDate previousStart, LocalDate previousEnd) {
        log.debug("Calculating profit growth for project {}", projectId);

        BigDecimal currentProfit = calculateProfit(projectId, currentStart, currentEnd);
        BigDecimal previousProfit = calculateProfit(projectId, previousStart, previousEnd);

        BigDecimal growthRate = calculateGrowthRate(currentProfit, previousProfit);
        log.debug("Profit growth: {}% (current: {}, previous: {})",
                growthRate, currentProfit, previousProfit);

        return growthRate;
    }

    /**
     * Calcola la crescita dei ricavi tra due periodi
     */
    public BigDecimal calculateRevenueGrowth(Long projectId,
                                              LocalDate currentStart, LocalDate currentEnd,
                                              LocalDate previousStart, LocalDate previousEnd) {
        log.debug("Calculating revenue growth for project {}", projectId);

        BigDecimal currentRevenue = calculateTotalRevenue(projectId, currentStart, currentEnd);
        BigDecimal previousRevenue = calculateTotalRevenue(projectId, previousStart, previousEnd);

        BigDecimal growthRate = calculateGrowthRate(currentRevenue, previousRevenue);
        log.debug("Revenue growth: {}% (current: {}, previous: {})",
                growthRate, currentRevenue, previousRevenue);

        return growthRate;
    }
}
