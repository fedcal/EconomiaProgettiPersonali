package dev.federicocalo.managementeconomy.service;

import dev.federicocalo.managementeconomy.dto.request.OneTimeCostRequest;
import dev.federicocalo.managementeconomy.dto.request.RecurringCostRequest;
import dev.federicocalo.managementeconomy.dto.response.OneTimeCostResponse;
import dev.federicocalo.managementeconomy.dto.response.RecurringCostResponse;
import dev.federicocalo.managementeconomy.entity.OneTimeCost;
import dev.federicocalo.managementeconomy.entity.Project;
import dev.federicocalo.managementeconomy.entity.RecurringCost;
import dev.federicocalo.managementeconomy.enums.CostCategory;
import dev.federicocalo.managementeconomy.exception.ResourceNotFoundException;
import dev.federicocalo.managementeconomy.mapper.CostMapper;
import dev.federicocalo.managementeconomy.repository.OneTimeCostRepository;
import dev.federicocalo.managementeconomy.repository.ProjectRepository;
import dev.federicocalo.managementeconomy.repository.RecurringCostRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service per la gestione dei costi (una tantum e ricorrenti)
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class CostService {

    private final OneTimeCostRepository oneTimeCostRepository;
    private final RecurringCostRepository recurringCostRepository;
    private final ProjectRepository projectRepository;
    private final CostMapper costMapper;

    // ========================== ONE-TIME COSTS ==========================

    /**
     * Crea un nuovo costo una tantum
     */
    public OneTimeCostResponse createOneTimeCost(OneTimeCostRequest request) {
        log.info("Creating one-time cost: {} for project {}", request.getName(), request.getProjectId());

        Project project = projectRepository.findById(request.getProjectId())
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));

        OneTimeCost cost = costMapper.toEntity(request);
        cost.setProject(project);

        OneTimeCost savedCost = oneTimeCostRepository.save(cost);
        log.info("One-time cost created successfully with id: {}", savedCost.getId());

        return costMapper.toResponse(savedCost);
    }

    /**
     * Aggiorna un costo una tantum esistente
     */
    public OneTimeCostResponse updateOneTimeCost(Long id, OneTimeCostRequest request) {
        log.info("Updating one-time cost with id: {}", id);

        OneTimeCost existingCost = oneTimeCostRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("OneTimeCost", "id", id));

        // Se il projectId è cambiato, verifica che esista
        if (!existingCost.getProject().getId().equals(request.getProjectId())) {
            Project newProject = projectRepository.findById(request.getProjectId())
                    .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));
            existingCost.setProject(newProject);
        }

        costMapper.updateEntityFromRequest(request, existingCost);
        OneTimeCost updatedCost = oneTimeCostRepository.save(existingCost);

        log.info("One-time cost updated successfully");
        return costMapper.toResponse(updatedCost);
    }

    /**
     * Trova un costo una tantum per ID
     */
    @Transactional(readOnly = true)
    public OneTimeCostResponse findOneTimeCostById(Long id) {
        log.debug("Finding one-time cost with id: {}", id);

        OneTimeCost cost = oneTimeCostRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("OneTimeCost", "id", id));

        return costMapper.toResponse(cost);
    }

    /**
     * Trova tutti i costi una tantum di un progetto
     */
    @Transactional(readOnly = true)
    public List<OneTimeCostResponse> findOneTimeCostsByProject(Long projectId) {
        log.debug("Finding all one-time costs for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        List<OneTimeCost> costs = oneTimeCostRepository.findByProjectId(projectId);
        return costs.stream()
                .map(costMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Trova costi una tantum per progetto e categoria
     */
    @Transactional(readOnly = true)
    public List<OneTimeCostResponse> findOneTimeCostsByProjectAndCategory(Long projectId, CostCategory category) {
        log.debug("Finding one-time costs for project {} and category {}", projectId, category);

        List<OneTimeCost> costs = oneTimeCostRepository.findByProjectIdAndCategory(projectId, category);
        return costs.stream()
                .map(costMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Trova costi una tantum per range di date
     */
    @Transactional(readOnly = true)
    public List<OneTimeCostResponse> findOneTimeCostsByDateRange(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Finding one-time costs for project {} between {} and {}", projectId, startDate, endDate);

        List<OneTimeCost> costs = oneTimeCostRepository.findByProjectIdAndDateRange(projectId, startDate, endDate);
        return costs.stream()
                .map(costMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Calcola totale costi una tantum per range di date
     */
    @Transactional(readOnly = true)
    public BigDecimal calculateOneTimeCostsTotalByDateRange(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Calculating total one-time costs for project {} between {} and {}", projectId, startDate, endDate);

        return oneTimeCostRepository.calculateTotalByDateRange(projectId, startDate, endDate);
    }

    /**
     * Elimina un costo una tantum
     */
    public void deleteOneTimeCost(Long id) {
        log.info("Deleting one-time cost with id: {}", id);

        if (!oneTimeCostRepository.existsById(id)) {
            throw new ResourceNotFoundException("OneTimeCost", "id", id);
        }

        oneTimeCostRepository.deleteById(id);
        log.info("One-time cost deleted successfully");
    }

    // ========================== RECURRING COSTS ==========================

    /**
     * Crea un nuovo costo ricorrente
     */
    public RecurringCostResponse createRecurringCost(RecurringCostRequest request) {
        log.info("Creating recurring cost: {} for project {}", request.getName(), request.getProjectId());

        Project project = projectRepository.findById(request.getProjectId())
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));

        RecurringCost cost = costMapper.toEntity(request);
        cost.setProject(project);

        RecurringCost savedCost = recurringCostRepository.save(cost);
        log.info("Recurring cost created successfully with id: {}", savedCost.getId());

        return costMapper.toResponse(savedCost);
    }

    /**
     * Aggiorna un costo ricorrente esistente
     */
    public RecurringCostResponse updateRecurringCost(Long id, RecurringCostRequest request) {
        log.info("Updating recurring cost with id: {}", id);

        RecurringCost existingCost = recurringCostRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("RecurringCost", "id", id));

        // Se il projectId è cambiato, verifica che esista
        if (!existingCost.getProject().getId().equals(request.getProjectId())) {
            Project newProject = projectRepository.findById(request.getProjectId())
                    .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));
            existingCost.setProject(newProject);
        }

        costMapper.updateEntityFromRequest(request, existingCost);
        RecurringCost updatedCost = recurringCostRepository.save(existingCost);

        log.info("Recurring cost updated successfully");
        return costMapper.toResponse(updatedCost);
    }

    /**
     * Trova un costo ricorrente per ID
     */
    @Transactional(readOnly = true)
    public RecurringCostResponse findRecurringCostById(Long id) {
        log.debug("Finding recurring cost with id: {}", id);

        RecurringCost cost = recurringCostRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("RecurringCost", "id", id));

        return costMapper.toResponse(cost);
    }

    /**
     * Trova tutti i costi ricorrenti di un progetto
     */
    @Transactional(readOnly = true)
    public List<RecurringCostResponse> findRecurringCostsByProject(Long projectId) {
        log.debug("Finding all recurring costs for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        List<RecurringCost> costs = recurringCostRepository.findByProjectId(projectId);
        return costs.stream()
                .map(costMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Trova costi ricorrenti attivi per un progetto
     */
    @Transactional(readOnly = true)
    public List<RecurringCostResponse> findActiveRecurringCosts(Long projectId) {
        log.debug("Finding active recurring costs for project: {}", projectId);

        List<RecurringCost> costs = recurringCostRepository.findActiveByProjectId(projectId);
        return costs.stream()
                .map(costMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Calcola totale mensile dei costi ricorrenti attivi
     */
    @Transactional(readOnly = true)
    public BigDecimal calculateMonthlyRecurringCostsTotal(Long projectId) {
        log.debug("Calculating monthly recurring costs total for project: {}", projectId);

        return recurringCostRepository.calculateTotalMonthlyActive(projectId);
    }

    /**
     * Disattiva un costo ricorrente
     */
    public RecurringCostResponse deactivateRecurringCost(Long id) {
        log.info("Deactivating recurring cost with id: {}", id);

        RecurringCost cost = recurringCostRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("RecurringCost", "id", id));

        cost.setIsActive(false);
        RecurringCost updatedCost = recurringCostRepository.save(cost);

        log.info("Recurring cost deactivated successfully");
        return costMapper.toResponse(updatedCost);
    }

    /**
     * Attiva un costo ricorrente
     */
    public RecurringCostResponse activateRecurringCost(Long id) {
        log.info("Activating recurring cost with id: {}", id);

        RecurringCost cost = recurringCostRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("RecurringCost", "id", id));

        cost.setIsActive(true);
        RecurringCost updatedCost = recurringCostRepository.save(cost);

        log.info("Recurring cost activated successfully");
        return costMapper.toResponse(updatedCost);
    }

    /**
     * Elimina un costo ricorrente
     */
    public void deleteRecurringCost(Long id) {
        log.info("Deleting recurring cost with id: {}", id);

        if (!recurringCostRepository.existsById(id)) {
            throw new ResourceNotFoundException("RecurringCost", "id", id);
        }

        recurringCostRepository.deleteById(id);
        log.info("Recurring cost deleted successfully");
    }
}
