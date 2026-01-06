package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.CalculatedMetric;
import dev.federicocalo.managementeconomy.enums.MetricType;
import dev.federicocalo.managementeconomy.enums.PeriodType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * Repository per metriche KPI calcolate
 */
@Repository
public interface CalculatedMetricRepository extends JpaRepository<CalculatedMetric, Long> {

    List<CalculatedMetric> findByProjectId(Long projectId);

    List<CalculatedMetric> findByProjectIdAndMetricType(Long projectId, MetricType metricType);

    List<CalculatedMetric> findByProjectIdAndPeriodType(Long projectId, PeriodType periodType);

    @Query("SELECT m FROM CalculatedMetric m WHERE m.project.id = :projectId " +
           "AND m.metricDate >= :startDate AND m.metricDate <= :endDate " +
           "ORDER BY m.metricDate ASC")
    List<CalculatedMetric> findByProjectIdAndDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT m FROM CalculatedMetric m WHERE m.project.id = :projectId " +
           "AND m.metricType = :metricType " +
           "AND m.metricDate >= :startDate AND m.metricDate <= :endDate " +
           "ORDER BY m.metricDate ASC")
    List<CalculatedMetric> findByProjectIdAndTypeAndDateRange(
        @Param("projectId") Long projectId,
        @Param("metricType") MetricType metricType,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT m FROM CalculatedMetric m WHERE m.project.id = :projectId " +
           "AND m.metricDate = :date AND m.metricType = :metricType AND m.periodType = :periodType")
    Optional<CalculatedMetric> findByProjectIdAndDateAndTypeAndPeriod(
        @Param("projectId") Long projectId,
        @Param("date") LocalDate date,
        @Param("metricType") MetricType metricType,
        @Param("periodType") PeriodType periodType
    );

    @Query("SELECT m FROM CalculatedMetric m WHERE m.project.id = :projectId " +
           "AND m.metricType = :metricType " +
           "ORDER BY m.metricDate DESC")
    List<CalculatedMetric> findLatestByType(
        @Param("projectId") Long projectId,
        @Param("metricType") MetricType metricType
    );

    void deleteByProjectIdAndMetricDate(Long projectId, LocalDate metricDate);
}
