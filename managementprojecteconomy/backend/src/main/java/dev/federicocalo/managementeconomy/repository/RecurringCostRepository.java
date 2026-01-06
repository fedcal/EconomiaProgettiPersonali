package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.RecurringCost;
import dev.federicocalo.managementeconomy.enums.CostCategory;
import dev.federicocalo.managementeconomy.enums.Frequency;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;

/**
 * Repository per costi ricorrenti
 */
@Repository
public interface RecurringCostRepository extends JpaRepository<RecurringCost, Long> {

    List<RecurringCost> findByProjectId(Long projectId);

    List<RecurringCost> findByProjectIdAndIsActive(Long projectId, Boolean isActive);

    List<RecurringCost> findByProjectIdAndCategory(Long projectId, CostCategory category);

    List<RecurringCost> findByProjectIdAndFrequency(Long projectId, Frequency frequency);

    @Query("SELECT c FROM RecurringCost c WHERE c.project.id = :projectId AND c.isActive = true")
    List<RecurringCost> findActiveByProjectId(@Param("projectId") Long projectId);

    @Query("SELECT COALESCE(SUM(c.amount), 0) FROM RecurringCost c " +
           "WHERE c.project.id = :projectId AND c.isActive = true AND c.frequency = 'MONTHLY'")
    BigDecimal calculateTotalMonthlyActive(@Param("projectId") Long projectId);

    @Query("SELECT c.category, SUM(c.amount) FROM RecurringCost c " +
           "WHERE c.project.id = :projectId AND c.isActive = true " +
           "GROUP BY c.category")
    List<Object[]> calculateActiveTotalByCategory(@Param("projectId") Long projectId);

    long countByProjectIdAndIsActive(Long projectId, Boolean isActive);
}
