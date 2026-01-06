package dev.federicocalo.managementeconomy.service;

import dev.federicocalo.managementeconomy.dto.request.RevenueStreamRequest;
import dev.federicocalo.managementeconomy.dto.response.RevenueStreamResponse;
import dev.federicocalo.managementeconomy.entity.Project;
import dev.federicocalo.managementeconomy.entity.RevenueStream;
import dev.federicocalo.managementeconomy.enums.RevenueType;
import dev.federicocalo.managementeconomy.exception.ResourceNotFoundException;
import dev.federicocalo.managementeconomy.mapper.RevenueMapper;
import dev.federicocalo.managementeconomy.repository.ProjectRepository;
import dev.federicocalo.managementeconomy.repository.RevenueStreamRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service per la gestione dei revenue streams
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class RevenueService {

    private final RevenueStreamRepository revenueStreamRepository;
    private final ProjectRepository projectRepository;
    private final RevenueMapper revenueMapper;

    /**
     * Crea un nuovo revenue stream
     */
    public RevenueStreamResponse create(RevenueStreamRequest request) {
        log.info("Creating revenue stream: {} for project {}", request.getName(), request.getProjectId());

        Project project = projectRepository.findById(request.getProjectId())
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));

        RevenueStream revenue = revenueMapper.toEntity(request);
        revenue.setProject(project);

        RevenueStream savedRevenue = revenueStreamRepository.save(revenue);
        log.info("Revenue stream created successfully with id: {}", savedRevenue.getId());

        return revenueMapper.toResponse(savedRevenue);
    }

    /**
     * Aggiorna un revenue stream esistente
     */
    public RevenueStreamResponse update(Long id, RevenueStreamRequest request) {
        log.info("Updating revenue stream with id: {}", id);

        RevenueStream existingRevenue = revenueStreamRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("RevenueStream", "id", id));

        // Se il projectId è cambiato, verifica che esista
        if (!existingRevenue.getProject().getId().equals(request.getProjectId())) {
            Project newProject = projectRepository.findById(request.getProjectId())
                    .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));
            existingRevenue.setProject(newProject);
        }

        revenueMapper.updateEntityFromRequest(request, existingRevenue);
        RevenueStream updatedRevenue = revenueStreamRepository.save(existingRevenue);

        log.info("Revenue stream updated successfully");
        return revenueMapper.toResponse(updatedRevenue);
    }

    /**
     * Trova un revenue stream per ID
     */
    @Transactional(readOnly = true)
    public RevenueStreamResponse findById(Long id) {
        log.debug("Finding revenue stream with id: {}", id);

        RevenueStream revenue = revenueStreamRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("RevenueStream", "id", id));

        return revenueMapper.toResponse(revenue);
    }

    /**
     * Trova tutti i revenue streams di un progetto
     */
    @Transactional(readOnly = true)
    public List<RevenueStreamResponse> findByProject(Long projectId) {
        log.debug("Finding all revenue streams for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        List<RevenueStream> revenues = revenueStreamRepository.findByProjectId(projectId);
        return revenues.stream()
                .map(revenueMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Trova revenue streams per progetto e tipo
     */
    @Transactional(readOnly = true)
    public List<RevenueStreamResponse> findByProjectAndType(Long projectId, RevenueType revenueType) {
        log.debug("Finding revenue streams for project {} and type {}", projectId, revenueType);

        List<RevenueStream> revenues = revenueStreamRepository.findByProjectIdAndRevenueType(projectId, revenueType);
        return revenues.stream()
                .map(revenueMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Trova revenue streams per range di date
     */
    @Transactional(readOnly = true)
    public List<RevenueStreamResponse> findByDateRange(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Finding revenue streams for project {} between {} and {}", projectId, startDate, endDate);

        List<RevenueStream> revenues = revenueStreamRepository.findByProjectIdAndDateRange(projectId, startDate, endDate);
        return revenues.stream()
                .map(revenueMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Calcola totale revenue per range di date
     */
    @Transactional(readOnly = true)
    public BigDecimal calculateTotalByDateRange(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating total revenue for project {} between {} and {}", projectId, startDate, endDate);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return revenueStreamRepository.calculateTotalByDateRange(projectId, startDate, endDate);
    }

    /**
     * Calcola revenue totali per tipo
     */
    @Transactional(readOnly = true)
    public List<Object[]> calculateTotalByType(Long projectId) {
        log.debug("Calculating revenue totals by type for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return revenueStreamRepository.calculateTotalByType(projectId);
    }

    /**
     * Calcola revenue totali per source
     */
    @Transactional(readOnly = true)
    public List<Object[]> calculateTotalBySource(Long projectId) {
        log.debug("Calculating revenue totals by source for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return revenueStreamRepository.calculateTotalBySource(projectId);
    }

    /**
     * Calcola revenue mensili
     */
    @Transactional(readOnly = true)
    public List<Object[]> calculateMonthlyRevenue(Long projectId) {
        log.debug("Calculating monthly revenue for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return revenueStreamRepository.calculateMonthlyRevenue(projectId);
    }

    /**
     * Elimina un revenue stream
     */
    public void delete(Long id) {
        log.info("Deleting revenue stream with id: {}", id);

        if (!revenueStreamRepository.existsById(id)) {
            throw new ResourceNotFoundException("RevenueStream", "id", id);
        }

        revenueStreamRepository.deleteById(id);
        log.info("Revenue stream deleted successfully");
    }
}
