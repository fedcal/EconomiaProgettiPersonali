package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.Booking;
import dev.federicocalo.managementeconomy.enums.BookingStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * Repository per gestione prenotazioni
 */
@Repository
public interface BookingRepository extends JpaRepository<Booking, Long> {

    /**
     * Trova tutte le prenotazioni di un progetto
     */
    List<Booking> findByProjectId(Long projectId);

    /**
     * Trova prenotazioni per progetto e stato
     */
    List<Booking> findByProjectIdAndBookingStatus(Long projectId, BookingStatus status);

    /**
     * Trova prenotazioni per piattaforma
     */
    List<Booking> findByPlatform(String platform);

    /**
     * Trova prenotazioni in un range di date (checkin)
     */
    @Query("SELECT b FROM Booking b WHERE b.project.id = :projectId " +
           "AND b.checkinDate >= :startDate AND b.checkinDate <= :endDate " +
           "ORDER BY b.checkinDate DESC")
    List<Booking> findByProjectIdAndDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    /**
     * Trova prenotazioni per anno (checkin)
     */
    @Query("SELECT b FROM Booking b WHERE b.project.id = :projectId " +
           "AND YEAR(b.checkinDate) = :year " +
           "ORDER BY b.checkinDate DESC")
    List<Booking> findByProjectIdAndYear(
        @Param("projectId") Long projectId,
        @Param("year") int year
    );

    /**
     * Calcola totale revenue netto per progetto e range date
     */
    @Query("SELECT COALESCE(SUM(b.netRevenue), 0) FROM Booking b " +
           "WHERE b.project.id = :projectId " +
           "AND b.bookingStatus IN ('CONFIRMED', 'COMPLETED') " +
           "AND b.checkinDate >= :startDate AND b.checkinDate <= :endDate")
    BigDecimal calculateTotalNetRevenueByDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    /**
     * Calcola totale notti per progetto e anno
     */
    @Query("SELECT COALESCE(SUM(b.nights), 0) FROM Booking b " +
           "WHERE b.project.id = :projectId " +
           "AND b.bookingStatus IN ('CONFIRMED', 'COMPLETED') " +
           "AND YEAR(b.checkinDate) = :year")
    Integer calculateTotalNightsByYear(
        @Param("projectId") Long projectId,
        @Param("year") int year
    );

    /**
     * Calcola totale prezzo lordo per progetto e range
     */
    @Query("SELECT COALESCE(SUM(b.price), 0) FROM Booking b " +
           "WHERE b.project.id = :projectId " +
           "AND b.bookingStatus IN ('CONFIRMED', 'COMPLETED') " +
           "AND b.checkinDate >= :startDate AND b.checkinDate <= :endDate")
    BigDecimal calculateTotalGrossRevenueByDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    /**
     * Calcola totale commissioni per progetto e range
     */
    @Query("SELECT COALESCE(SUM(b.commissionAmount), 0) FROM Booking b " +
           "WHERE b.project.id = :projectId " +
           "AND b.bookingStatus IN ('CONFIRMED', 'COMPLETED') " +
           "AND b.checkinDate >= :startDate AND b.checkinDate <= :endDate")
    BigDecimal calculateTotalCommissionsByDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    /**
     * Calcola totale revenue (alias per calculateTotalGrossRevenueByDateRange)
     */
    default BigDecimal calculateTotalRevenueByDateRange(Long projectId, LocalDate startDate, LocalDate endDate) {
        return calculateTotalGrossRevenueByDateRange(projectId, startDate, endDate);
    }

    /**
     * Calcola totale notti per progetto e range date
     */
    @Query("SELECT COALESCE(SUM(b.nights), 0) FROM Booking b " +
           "WHERE b.project.id = :projectId " +
           "AND b.bookingStatus IN ('CONFIRMED', 'COMPLETED') " +
           "AND b.checkinDate >= :startDate AND b.checkinDate <= :endDate")
    Integer calculateTotalNightsByDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    /**
     * Conta prenotazioni per progetto e stato
     */
    long countByProjectIdAndBookingStatus(Long projectId, BookingStatus status);

    /**
     * Trova prenotazioni per progetto e piattaforma
     */
    List<Booking> findByProjectIdAndPlatform(Long projectId, String platform);

    /**
     * Verifica sovrapposizioni date (per evitare double booking)
     */
    @Query("SELECT COUNT(b) > 0 FROM Booking b WHERE b.project.id = :projectId " +
           "AND b.bookingStatus IN ('CONFIRMED', 'PENDING') " +
           "AND ((b.checkinDate <= :checkoutDate AND b.checkoutDate >= :checkinDate))")
    boolean existsOverlappingBooking(
        @Param("projectId") Long projectId,
        @Param("checkinDate") LocalDate checkinDate,
        @Param("checkoutDate") LocalDate checkoutDate
    );
}
