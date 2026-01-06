package dev.federicocalo.managementeconomy.service;

import dev.federicocalo.managementeconomy.entity.CalculatedMetric;
import dev.federicocalo.managementeconomy.entity.Project;
import dev.federicocalo.managementeconomy.enums.MetricType;
import dev.federicocalo.managementeconomy.enums.PeriodType;
import dev.federicocalo.managementeconomy.exception.ResourceNotFoundException;
import dev.federicocalo.managementeconomy.repository.CalculatedMetricRepository;
import dev.federicocalo.managementeconomy.repository.ProjectRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * Service per la gestione delle metriche KPI calcolate
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class CalculatedMetricService {

    private final CalculatedMetricRepository calculatedMetricRepository;
    private final ProjectRepository projectRepository;

    /**
     * Salva o aggiorna una metrica calcolata
     */
    public CalculatedMetric saveOrUpdate(Long projectId, LocalDate metricDate, MetricType metricType,
                                          BigDecimal metricValue, PeriodType periodType) {
        log.info("Saving metric {} for project {} on date {} with period {}",
                metricType, projectId, metricDate, periodType);

        Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        // Verifica se esiste già una metrica con stessi parametri
        Optional<CalculatedMetric> existing = calculatedMetricRepository.findByProjectIdAndDateAndTypeAndPeriod(
                projectId, metricDate, metricType, periodType
        );

        if (existing.isPresent()) {
            log.debug("Updating existing metric with id: {}", existing.get().getId());
            CalculatedMetric existingMetric = existing.get();
            existingMetric.setMetricValue(metricValue);
            return calculatedMetricRepository.save(existingMetric);
        } else {
            log.debug("Creating new metric record");
            CalculatedMetric newMetric = CalculatedMetric.builder()
                    .project(project)
                    .metricDate(metricDate)
                    .metricType(metricType)
                    .metricValue(metricValue)
                    .periodType(periodType)
                    .build();
            return calculatedMetricRepository.save(newMetric);
        }
    }

    /**
     * Trova tutte le metriche per un progetto
     */
    @Transactional(readOnly = true)
    public List<CalculatedMetric> findByProject(Long projectId) {
        log.debug("Finding all metrics for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return calculatedMetricRepository.findByProjectId(projectId);
    }

    /**
     * Trova metriche per tipo
     */
    @Transactional(readOnly = true)
    public List<CalculatedMetric> findByType(Long projectId, MetricType metricType) {
        log.debug("Finding metrics of type {} for project: {}", metricType, projectId);

        return calculatedMetricRepository.findByProjectIdAndMetricType(projectId, metricType);
    }

    /**
     * Trova metriche per periodo
     */
    @Transactional(readOnly = true)
    public List<CalculatedMetric> findByPeriod(Long projectId, PeriodType periodType) {
        log.debug("Finding metrics for period {} for project: {}", periodType, projectId);

        return calculatedMetricRepository.findByProjectIdAndPeriodType(projectId, periodType);
    }

    /**
     * Trova metriche per range di date
     */
    @Transactional(readOnly = true)
    public List<CalculatedMetric> findByDateRange(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Finding metrics for project {} between {} and {}", projectId, startDate, endDate);

        return calculatedMetricRepository.findByProjectIdAndDateRange(projectId, startDate, endDate);
    }

    /**
     * Trova metriche per tipo e range di date
     */
    @Transactional(readOnly = true)
    public List<CalculatedMetric> findByTypeAndDateRange(Long projectId, MetricType metricType,
                                                          LocalDate startDate, LocalDate endDate) {
        log.debug("Finding metrics of type {} for project {} between {} and {}",
                metricType, projectId, startDate, endDate);

        return calculatedMetricRepository.findByProjectIdAndTypeAndDateRange(projectId, metricType, startDate, endDate);
    }

    /**
     * Trova l'ultima metrica di un tipo specifico
     */
    @Transactional(readOnly = true)
    public Optional<CalculatedMetric> findLatestByType(Long projectId, MetricType metricType) {
        log.debug("Finding latest metric of type {} for project: {}", metricType, projectId);

        List<CalculatedMetric> metrics = calculatedMetricRepository.findLatestByType(projectId, metricType);
        return metrics.isEmpty() ? Optional.empty() : Optional.of(metrics.get(0));
    }

    /**
     * Elimina metriche per una data specifica
     */
    public void deleteByDate(Long projectId, LocalDate metricDate) {
        log.info("Deleting metrics for project {} on date {}", projectId, metricDate);

        calculatedMetricRepository.deleteByProjectIdAndMetricDate(projectId, metricDate);
        log.info("Metrics deleted successfully");
    }

    /**
     * Importa batch di metriche
     */
    public void importBatch(List<CalculatedMetric> metrics) {
        log.info("Importing {} calculated metrics", metrics.size());

        for (CalculatedMetric metric : metrics) {
            saveOrUpdate(
                    metric.getProject().getId(),
                    metric.getMetricDate(),
                    metric.getMetricType(),
                    metric.getMetricValue(),
                    metric.getPeriodType()
            );
        }

        log.info("Metrics import completed");
    }
}
