package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.Subscription;
import dev.federicocalo.managementeconomy.enums.SubscriptionStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.util.List;

/**
 * Repository per subscriptions (SaaS)
 */
@Repository
public interface SubscriptionRepository extends JpaRepository<Subscription, Long> {

    List<Subscription> findByProjectId(Long projectId);

    List<Subscription> findByProjectIdAndSubscriptionStatus(Long projectId, SubscriptionStatus status);

    @Query("SELECT s FROM Subscription s WHERE s.project.id = :projectId AND s.subscriptionStatus = 'ACTIVE'")
    List<Subscription> findActiveByProjectId(@Param("projectId") Long projectId);

    @Query("SELECT COALESCE(SUM(s.mrr), 0) FROM Subscription s " +
           "WHERE s.project.id = :projectId AND s.subscriptionStatus = 'ACTIVE'")
    BigDecimal calculateTotalMRR(@Param("projectId") Long projectId);

    @Query("SELECT COUNT(s) FROM Subscription s " +
           "WHERE s.project.id = :projectId AND s.subscriptionStatus = 'ACTIVE'")
    long countActiveSubscriptions(@Param("projectId") Long projectId);

    @Query("SELECT s.planName, COUNT(s) FROM Subscription s " +
           "WHERE s.project.id = :projectId AND s.subscriptionStatus = 'ACTIVE' " +
           "GROUP BY s.planName")
    List<Object[]> countSubscriptionsByPlan(@Param("projectId") Long projectId);

    @Query("SELECT s.planName, SUM(s.mrr) FROM Subscription s " +
           "WHERE s.project.id = :projectId AND s.subscriptionStatus = 'ACTIVE' " +
           "GROUP BY s.planName")
    List<Object[]> calculateMRRByPlan(@Param("projectId") Long projectId);

    long countByProjectIdAndSubscriptionStatus(Long projectId, SubscriptionStatus status);
}
