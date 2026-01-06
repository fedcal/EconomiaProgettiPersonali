package dev.federicocalo.managementeconomy.controller;

import dev.federicocalo.managementeconomy.dto.request.OneTimeCostRequest;
import dev.federicocalo.managementeconomy.dto.request.RecurringCostRequest;
import dev.federicocalo.managementeconomy.dto.response.OneTimeCostResponse;
import dev.federicocalo.managementeconomy.dto.response.RecurringCostResponse;
import dev.federicocalo.managementeconomy.enums.CostCategory;
import dev.federicocalo.managementeconomy.service.CostService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

/**
 * REST Controller per la gestione dei costi (una tantum e ricorrenti)
 */
@RestController
@RequestMapping("/api/v1/costs")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*")
public class CostController {

    private final CostService costService;

    // ========================== ONE-TIME COSTS ==========================

    /**
     * POST /api/v1/costs/one-time - Crea un nuovo costo una tantum
     */
    @PostMapping("/one-time")
    public ResponseEntity<OneTimeCostResponse> createOneTimeCost(@Valid @RequestBody OneTimeCostRequest request) {
        log.info("REST: Creating one-time cost: {}", request.getName());
        OneTimeCostResponse response = costService.createOneTimeCost(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    /**
     * PUT /api/v1/costs/one-time/{id} - Aggiorna un costo una tantum
     */
    @PutMapping("/one-time/{id}")
    public ResponseEntity<OneTimeCostResponse> updateOneTimeCost(
            @PathVariable Long id,
            @Valid @RequestBody OneTimeCostRequest request) {
        log.info("REST: Updating one-time cost with id: {}", id);
        OneTimeCostResponse response = costService.updateOneTimeCost(id, request);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/costs/one-time/{id} - Ottiene un costo una tantum per ID
     */
    @GetMapping("/one-time/{id}")
    public ResponseEntity<OneTimeCostResponse> getOneTimeCostById(@PathVariable Long id) {
        log.info("REST: Getting one-time cost with id: {}", id);
        OneTimeCostResponse response = costService.findOneTimeCostById(id);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/costs/one-time/project/{projectId} - Ottiene tutti i costi una tantum di un progetto
     */
    @GetMapping("/one-time/project/{projectId}")
    public ResponseEntity<List<OneTimeCostResponse>> getOneTimeCostsByProject(@PathVariable Long projectId) {
        log.info("REST: Getting all one-time costs for project: {}", projectId);
        List<OneTimeCostResponse> response = costService.findOneTimeCostsByProject(projectId);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/costs/one-time/project/{projectId}/category/{category} - Ottiene costi una tantum per categoria
     */
    @GetMapping("/one-time/project/{projectId}/category/{category}")
    public ResponseEntity<List<OneTimeCostResponse>> getOneTimeCostsByCategory(
            @PathVariable Long projectId,
            @PathVariable CostCategory category) {
        log.info("REST: Getting one-time costs for project {} and category {}", projectId, category);
        List<OneTimeCostResponse> response = costService.findOneTimeCostsByProjectAndCategory(projectId, category);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/costs/one-time/project/{projectId}/date-range - Ottiene costi una tantum per range di date
     */
    @GetMapping("/one-time/project/{projectId}/date-range")
    public ResponseEntity<List<OneTimeCostResponse>> getOneTimeCostsByDateRange(
            @PathVariable Long projectId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        log.info("REST: Getting one-time costs for project {} between {} and {}", projectId, startDate, endDate);
        List<OneTimeCostResponse> response = costService.findOneTimeCostsByDateRange(projectId, startDate, endDate);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/costs/one-time/project/{projectId}/total - Calcola totale costi una tantum per range di date
     */
    @GetMapping("/one-time/project/{projectId}/total")
    public ResponseEntity<Map<String, BigDecimal>> getOneTimeCostsTotal(
            @PathVariable Long projectId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        log.info("REST: Calculating total one-time costs for project {} between {} and {}", projectId, startDate, endDate);
        BigDecimal total = costService.calculateOneTimeCostsTotalByDateRange(projectId, startDate, endDate);
        return ResponseEntity.ok(Map.of("total", total));
    }

    /**
     * DELETE /api/v1/costs/one-time/{id} - Elimina un costo una tantum
     */
    @DeleteMapping("/one-time/{id}")
    public ResponseEntity<Void> deleteOneTimeCost(@PathVariable Long id) {
        log.info("REST: Deleting one-time cost with id: {}", id);
        costService.deleteOneTimeCost(id);
        return ResponseEntity.noContent().build();
    }

    // ========================== RECURRING COSTS ==========================

    /**
     * POST /api/v1/costs/recurring - Crea un nuovo costo ricorrente
     */
    @PostMapping("/recurring")
    public ResponseEntity<RecurringCostResponse> createRecurringCost(@Valid @RequestBody RecurringCostRequest request) {
        log.info("REST: Creating recurring cost: {}", request.getName());
        RecurringCostResponse response = costService.createRecurringCost(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    /**
     * PUT /api/v1/costs/recurring/{id} - Aggiorna un costo ricorrente
     */
    @PutMapping("/recurring/{id}")
    public ResponseEntity<RecurringCostResponse> updateRecurringCost(
            @PathVariable Long id,
            @Valid @RequestBody RecurringCostRequest request) {
        log.info("REST: Updating recurring cost with id: {}", id);
        RecurringCostResponse response = costService.updateRecurringCost(id, request);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/costs/recurring/{id} - Ottiene un costo ricorrente per ID
     */
    @GetMapping("/recurring/{id}")
    public ResponseEntity<RecurringCostResponse> getRecurringCostById(@PathVariable Long id) {
        log.info("REST: Getting recurring cost with id: {}", id);
        RecurringCostResponse response = costService.findRecurringCostById(id);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/costs/recurring/project/{projectId} - Ottiene tutti i costi ricorrenti di un progetto
     */
    @GetMapping("/recurring/project/{projectId}")
    public ResponseEntity<List<RecurringCostResponse>> getRecurringCostsByProject(@PathVariable Long projectId) {
        log.info("REST: Getting all recurring costs for project: {}", projectId);
        List<RecurringCostResponse> response = costService.findRecurringCostsByProject(projectId);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/costs/recurring/project/{projectId}/active - Ottiene costi ricorrenti attivi
     */
    @GetMapping("/recurring/project/{projectId}/active")
    public ResponseEntity<List<RecurringCostResponse>> getActiveRecurringCosts(@PathVariable Long projectId) {
        log.info("REST: Getting active recurring costs for project: {}", projectId);
        List<RecurringCostResponse> response = costService.findActiveRecurringCosts(projectId);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/costs/recurring/project/{projectId}/monthly-total - Calcola totale mensile costi ricorrenti attivi
     */
    @GetMapping("/recurring/project/{projectId}/monthly-total")
    public ResponseEntity<Map<String, BigDecimal>> getMonthlyRecurringCostsTotal(@PathVariable Long projectId) {
        log.info("REST: Calculating monthly recurring costs total for project: {}", projectId);
        BigDecimal total = costService.calculateMonthlyRecurringCostsTotal(projectId);
        return ResponseEntity.ok(Map.of("monthlyTotal", total));
    }

    /**
     * PATCH /api/v1/costs/recurring/{id}/deactivate - Disattiva un costo ricorrente
     */
    @PatchMapping("/recurring/{id}/deactivate")
    public ResponseEntity<RecurringCostResponse> deactivateRecurringCost(@PathVariable Long id) {
        log.info("REST: Deactivating recurring cost with id: {}", id);
        RecurringCostResponse response = costService.deactivateRecurringCost(id);
        return ResponseEntity.ok(response);
    }

    /**
     * PATCH /api/v1/costs/recurring/{id}/activate - Attiva un costo ricorrente
     */
    @PatchMapping("/recurring/{id}/activate")
    public ResponseEntity<RecurringCostResponse> activateRecurringCost(@PathVariable Long id) {
        log.info("REST: Activating recurring cost with id: {}", id);
        RecurringCostResponse response = costService.activateRecurringCost(id);
        return ResponseEntity.ok(response);
    }

    /**
     * DELETE /api/v1/costs/recurring/{id} - Elimina un costo ricorrente
     */
    @DeleteMapping("/recurring/{id}")
    public ResponseEntity<Void> deleteRecurringCost(@PathVariable Long id) {
        log.info("REST: Deleting recurring cost with id: {}", id);
        costService.deleteRecurringCost(id);
        return ResponseEntity.noContent().build();
    }
}
