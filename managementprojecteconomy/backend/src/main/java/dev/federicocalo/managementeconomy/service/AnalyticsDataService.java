package dev.federicocalo.managementeconomy.service;

import dev.federicocalo.managementeconomy.entity.AnalyticsData;
import dev.federicocalo.managementeconomy.entity.Project;
import dev.federicocalo.managementeconomy.exception.ResourceNotFoundException;
import dev.federicocalo.managementeconomy.repository.AnalyticsDataRepository;
import dev.federicocalo.managementeconomy.repository.ProjectRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * Service per la gestione dei dati analytics (Google Analytics)
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class AnalyticsDataService {

    private final AnalyticsDataRepository analyticsDataRepository;
    private final ProjectRepository projectRepository;

    /**
     * Salva o aggiorna dati analytics
     */
    public AnalyticsData saveOrUpdate(AnalyticsData analyticsData) {
        log.info("Saving analytics data for project {} on date {}",
                analyticsData.getProject().getId(), analyticsData.getReportDate());

        // Verifica se esiste già un record con stessi parametri
        Optional<AnalyticsData> existing = analyticsDataRepository.findByProjectIdAndDateAndDeviceAndSource(
                analyticsData.getProject().getId(),
                analyticsData.getReportDate(),
                analyticsData.getDeviceType(),
                analyticsData.getTrafficSource()
        );

        if (existing.isPresent()) {
            log.debug("Updating existing analytics data with id: {}", existing.get().getId());
            AnalyticsData existingData = existing.get();
            existingData.setUsers(analyticsData.getUsers());
            existingData.setSessions(analyticsData.getSessions());
            existingData.setPageviews(analyticsData.getPageviews());
            existingData.setBounceRate(analyticsData.getBounceRate());
            existingData.setConversions(analyticsData.getConversions());
            return analyticsDataRepository.save(existingData);
        } else {
            log.debug("Creating new analytics data record");
            return analyticsDataRepository.save(analyticsData);
        }
    }

    /**
     * Importa batch di dati analytics
     */
    public void importBatch(Long projectId, List<AnalyticsData> dataList) {
        log.info("Importing {} analytics records for project {}", dataList.size(), projectId);

        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        for (AnalyticsData data : dataList) {
            data.setProject(project);
            saveOrUpdate(data);
        }

        log.info("Analytics data import completed");
    }

    /**
     * Trova dati analytics per progetto
     */
    @Transactional(readOnly = true)
    public List<AnalyticsData> findByProject(Long projectId) {
        log.debug("Finding analytics data for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return analyticsDataRepository.findByProjectId(projectId);
    }

    /**
     * Trova dati analytics per range di date
     */
    @Transactional(readOnly = true)
    public List<AnalyticsData> findByDateRange(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Finding analytics data for project {} between {} and {}", projectId, startDate, endDate);

        return analyticsDataRepository.findByProjectIdAndDateRange(projectId, startDate, endDate);
    }

    /**
     * Calcola totale utenti per periodo
     */
    @Transactional(readOnly = true)
    public Long calculateTotalUsers(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating total users for project {} between {} and {}", projectId, startDate, endDate);

        Long total = analyticsDataRepository.calculateTotalUsers(projectId, startDate, endDate);
        return total != null ? total : 0L;
    }

    /**
     * Calcola totale sessioni per periodo
     */
    @Transactional(readOnly = true)
    public Long calculateTotalSessions(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating total sessions for project {} between {} and {}", projectId, startDate, endDate);

        Long total = analyticsDataRepository.calculateTotalSessions(projectId, startDate, endDate);
        return total != null ? total : 0L;
    }

    /**
     * Calcola totale pageviews per periodo
     */
    @Transactional(readOnly = true)
    public Long calculateTotalPageviews(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating total pageviews for project {} between {} and {}", projectId, startDate, endDate);

        Long total = analyticsDataRepository.calculateTotalPageviews(projectId, startDate, endDate);
        return total != null ? total : 0L;
    }

    /**
     * Calcola utenti per traffic source
     */
    @Transactional(readOnly = true)
    public List<Object[]> calculateUsersByTrafficSource(Long projectId) {
        log.debug("Calculating users by traffic source for project: {}", projectId);

        return analyticsDataRepository.calculateUsersByTrafficSource(projectId);
    }

    /**
     * Calcola sessioni per device type
     */
    @Transactional(readOnly = true)
    public List<Object[]> calculateSessionsByDeviceType(Long projectId) {
        log.debug("Calculating sessions by device type for project: {}", projectId);

        return analyticsDataRepository.calculateSessionsByDeviceType(projectId);
    }

    /**
     * Calcola metriche mensili
     */
    @Transactional(readOnly = true)
    public List<Object[]> calculateMonthlyMetrics(Long projectId) {
        log.debug("Calculating monthly metrics for project: {}", projectId);

        return analyticsDataRepository.calculateMonthlyMetrics(projectId);
    }

    /**
     * Elimina dati analytics per una data specifica
     */
    public void deleteByDate(Long projectId, LocalDate reportDate) {
        log.info("Deleting analytics data for project {} on date {}", projectId, reportDate);

        analyticsDataRepository.deleteByProjectIdAndReportDate(projectId, reportDate);
        log.info("Analytics data deleted successfully");
    }
}
