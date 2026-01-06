package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.AnalyticsData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * Repository per analytics data (Google Analytics)
 */
@Repository
public interface AnalyticsDataRepository extends JpaRepository<AnalyticsData, Long> {

    List<AnalyticsData> findByProjectId(Long projectId);

    @Query("SELECT a FROM AnalyticsData a WHERE a.project.id = :projectId " +
           "AND a.reportDate >= :startDate AND a.reportDate <= :endDate " +
           "ORDER BY a.reportDate ASC")
    List<AnalyticsData> findByProjectIdAndDateRange(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT a FROM AnalyticsData a WHERE a.project.id = :projectId " +
           "AND a.reportDate = :date AND a.deviceType = :deviceType AND a.trafficSource = :trafficSource")
    Optional<AnalyticsData> findByProjectIdAndDateAndDeviceAndSource(
        @Param("projectId") Long projectId,
        @Param("date") LocalDate date,
        @Param("deviceType") String deviceType,
        @Param("trafficSource") String trafficSource
    );

    @Query("SELECT SUM(a.users) FROM AnalyticsData a " +
           "WHERE a.project.id = :projectId " +
           "AND a.reportDate >= :startDate AND a.reportDate <= :endDate")
    Long calculateTotalUsers(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT SUM(a.sessions) FROM AnalyticsData a " +
           "WHERE a.project.id = :projectId " +
           "AND a.reportDate >= :startDate AND a.reportDate <= :endDate")
    Long calculateTotalSessions(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT SUM(a.pageviews) FROM AnalyticsData a " +
           "WHERE a.project.id = :projectId " +
           "AND a.reportDate >= :startDate AND a.reportDate <= :endDate")
    Long calculateTotalPageviews(
        @Param("projectId") Long projectId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );

    @Query("SELECT a.trafficSource, SUM(a.users) FROM AnalyticsData a " +
           "WHERE a.project.id = :projectId " +
           "GROUP BY a.trafficSource " +
           "ORDER BY SUM(a.users) DESC")
    List<Object[]> calculateUsersByTrafficSource(@Param("projectId") Long projectId);

    @Query("SELECT a.deviceType, SUM(a.sessions) FROM AnalyticsData a " +
           "WHERE a.project.id = :projectId " +
           "GROUP BY a.deviceType " +
           "ORDER BY SUM(a.sessions) DESC")
    List<Object[]> calculateSessionsByDeviceType(@Param("projectId") Long projectId);

    @Query("SELECT YEAR(a.reportDate), MONTH(a.reportDate), SUM(a.users), SUM(a.sessions), SUM(a.pageviews) " +
           "FROM AnalyticsData a " +
           "WHERE a.project.id = :projectId " +
           "GROUP BY YEAR(a.reportDate), MONTH(a.reportDate) " +
           "ORDER BY YEAR(a.reportDate), MONTH(a.reportDate)")
    List<Object[]> calculateMonthlyMetrics(@Param("projectId") Long projectId);

    void deleteByProjectIdAndReportDate(Long projectId, LocalDate reportDate);
}
