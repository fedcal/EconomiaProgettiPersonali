package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.OneTimeCost;
import dev.federicocalo.managementeconomy.enums.CostCategory;
import dev.federicocalo.managementeconomy.enums.PaymentStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * Repository per costi una tantum
 */
@Repository
public interface OneTimeCostRepository extends JpaRepository<OneTimeCost, Long> {

    List<OneTimeCost> findByProjectId(Long projectId);

    List<OneTimeCost> findByProjectIdAndCategory(Long projectId, CostCategory category);

    List<OneTimeCost> findByProjectIdAndPaymentStatus(Long projectId, PaymentStatus status);

    @Query("SELECT c FROM OneTimeCost c WHERE c.project.id = :projectId " +
           "AND c.costDate >= :startDate AND c.costDate <= :endDate " +
           "ORDER BY c.costDate DESC")
    List<OneTimeCost> findByProjectIdAndDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT COALESCE(SUM(c.amount), 0) FROM OneTimeCost c " +
           "WHERE c.project.id = :projectId " +
           "AND c.costDate >= :startDate AND c.costDate <= :endDate")
    BigDecimal calculateTotalByDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT c.category, SUM(c.amount) FROM OneTimeCost c " +
           "WHERE c.project.id = :projectId " +
           "GROUP BY c.category")
    List<Object[]> calculateTotalByCategory(@Param("projectId") Long projectId);

    long countByProjectId(Long projectId);
}
