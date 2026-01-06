package dev.federicocalo.managementeconomy.controller;

import dev.federicocalo.managementeconomy.dto.request.SubscriptionRequest;
import dev.federicocalo.managementeconomy.dto.response.SubscriptionResponse;
import dev.federicocalo.managementeconomy.service.SubscriptionService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * REST Controller per la gestione delle subscriptions (SaaS)
 */
@RestController
@RequestMapping("/api/v1/subscriptions")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*")
public class SubscriptionController {

    private final SubscriptionService subscriptionService;

    /**
     * POST /api/v1/subscriptions - Crea una nuova subscription
     */
    @PostMapping
    public ResponseEntity<SubscriptionResponse> create(@Valid @RequestBody SubscriptionRequest request) {
        log.info("REST: Creating subscription for customer: {}", request.getCustomerName());
        SubscriptionResponse response = subscriptionService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    /**
     * PUT /api/v1/subscriptions/{id} - Aggiorna una subscription
     */
    @PutMapping("/{id}")
    public ResponseEntity<SubscriptionResponse> update(
            @PathVariable Long id,
            @Valid @RequestBody SubscriptionRequest request) {
        log.info("REST: Updating subscription with id: {}", id);
        SubscriptionResponse response = subscriptionService.update(id, request);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/subscriptions/{id} - Ottiene una subscription per ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<SubscriptionResponse> getById(@PathVariable Long id) {
        log.info("REST: Getting subscription with id: {}", id);
        SubscriptionResponse response = subscriptionService.findById(id);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/subscriptions/project/{projectId} - Ottiene tutte le subscriptions di un progetto
     */
    @GetMapping("/project/{projectId}")
    public ResponseEntity<List<SubscriptionResponse>> getByProject(@PathVariable Long projectId) {
        log.info("REST: Getting all subscriptions for project: {}", projectId);
        List<SubscriptionResponse> response = subscriptionService.findByProject(projectId);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/subscriptions/project/{projectId}/active - Ottiene subscriptions attive
     */
    @GetMapping("/project/{projectId}/active")
    public ResponseEntity<List<SubscriptionResponse>> getActiveSubscriptions(@PathVariable Long projectId) {
        log.info("REST: Getting active subscriptions for project: {}", projectId);
        List<SubscriptionResponse> response = subscriptionService.findActiveSubscriptions(projectId);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/subscriptions/project/{projectId}/mrr - Calcola MRR totale
     */
    @GetMapping("/project/{projectId}/mrr")
    public ResponseEntity<Map<String, BigDecimal>> getTotalMRR(@PathVariable Long projectId) {
        log.info("REST: Calculating total MRR for project: {}", projectId);
        BigDecimal totalMRR = subscriptionService.calculateTotalMRR(projectId);
        return ResponseEntity.ok(Map.of("totalMRR", totalMRR));
    }

    /**
     * GET /api/v1/subscriptions/project/{projectId}/count-active - Conta subscriptions attive
     */
    @GetMapping("/project/{projectId}/count-active")
    public ResponseEntity<Map<String, Long>> countActiveSubscriptions(@PathVariable Long projectId) {
        log.info("REST: Counting active subscriptions for project: {}", projectId);
        long count = subscriptionService.countActiveSubscriptions(projectId);
        return ResponseEntity.ok(Map.of("activeCount", count));
    }

    /**
     * GET /api/v1/subscriptions/project/{projectId}/count-by-plan - Conta subscriptions per piano
     */
    @GetMapping("/project/{projectId}/count-by-plan")
    public ResponseEntity<Map<String, Long>> countByPlan(@PathVariable Long projectId) {
        log.info("REST: Counting subscriptions by plan for project: {}", projectId);
        List<Object[]> results = subscriptionService.countSubscriptionsByPlan(projectId);

        Map<String, Long> countByPlan = new HashMap<>();
        for (Object[] result : results) {
            String planName = (String) result[0];
            Long count = (Long) result[1];
            countByPlan.put(planName, count);
        }

        return ResponseEntity.ok(countByPlan);
    }

    /**
     * GET /api/v1/subscriptions/project/{projectId}/mrr-by-plan - Calcola MRR per piano
     */
    @GetMapping("/project/{projectId}/mrr-by-plan")
    public ResponseEntity<Map<String, BigDecimal>> getMRRByPlan(@PathVariable Long projectId) {
        log.info("REST: Calculating MRR by plan for project: {}", projectId);
        List<Object[]> results = subscriptionService.calculateMRRByPlan(projectId);

        Map<String, BigDecimal> mrrByPlan = new HashMap<>();
        for (Object[] result : results) {
            String planName = (String) result[0];
            BigDecimal mrr = (BigDecimal) result[1];
            mrrByPlan.put(planName, mrr);
        }

        return ResponseEntity.ok(mrrByPlan);
    }

    /**
     * PATCH /api/v1/subscriptions/{id}/cancel - Cancella una subscription
     */
    @PatchMapping("/{id}/cancel")
    public ResponseEntity<SubscriptionResponse> cancel(@PathVariable Long id) {
        log.info("REST: Cancelling subscription with id: {}", id);
        SubscriptionResponse response = subscriptionService.cancel(id);
        return ResponseEntity.ok(response);
    }

    /**
     * PATCH /api/v1/subscriptions/{id}/reactivate - Riattiva una subscription
     */
    @PatchMapping("/{id}/reactivate")
    public ResponseEntity<SubscriptionResponse> reactivate(@PathVariable Long id) {
        log.info("REST: Reactivating subscription with id: {}", id);
        SubscriptionResponse response = subscriptionService.reactivate(id);
        return ResponseEntity.ok(response);
    }

    /**
     * DELETE /api/v1/subscriptions/{id} - Elimina una subscription
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("REST: Deleting subscription with id: {}", id);
        subscriptionService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
