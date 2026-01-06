package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.RevenueStream;
import dev.federicocalo.managementeconomy.enums.RevenueType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * Repository per revenue streams
 */
@Repository
public interface RevenueStreamRepository extends JpaRepository<RevenueStream, Long> {

    List<RevenueStream> findByProjectId(Long projectId);

    List<RevenueStream> findByProjectIdAndRevenueType(Long projectId, RevenueType revenueType);

    @Query("SELECT r FROM RevenueStream r WHERE r.project.id = :projectId " +
           "AND r.revenueDate >= :startDate AND r.revenueDate <= :endDate " +
           "ORDER BY r.revenueDate DESC")
    List<RevenueStream> findByProjectIdAndDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT COALESCE(SUM(r.amount), 0) FROM RevenueStream r " +
           "WHERE r.project.id = :projectId " +
           "AND r.revenueDate >= :startDate AND r.revenueDate <= :endDate")
    BigDecimal calculateTotalByDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT r.revenueType, SUM(r.amount) FROM RevenueStream r " +
           "WHERE r.project.id = :projectId " +
           "GROUP BY r.revenueType")
    List<Object[]> calculateTotalByType(@Param("projectId") Long projectId);

    @Query("SELECT r.source, SUM(r.amount) FROM RevenueStream r " +
           "WHERE r.project.id = :projectId " +
           "GROUP BY r.source")
    List<Object[]> calculateTotalBySource(@Param("projectId") Long projectId);

    @Query("SELECT YEAR(r.revenueDate), MONTH(r.revenueDate), SUM(r.amount) " +
           "FROM RevenueStream r " +
           "WHERE r.project.id = :projectId " +
           "GROUP BY YEAR(r.revenueDate), MONTH(r.revenueDate) " +
           "ORDER BY YEAR(r.revenueDate), MONTH(r.revenueDate)")
    List<Object[]> calculateMonthlyRevenue(@Param("projectId") Long projectId);

    long countByProjectId(Long projectId);
}
