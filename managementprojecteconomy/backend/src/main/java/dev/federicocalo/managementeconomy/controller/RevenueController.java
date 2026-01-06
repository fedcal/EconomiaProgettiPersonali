package dev.federicocalo.managementeconomy.controller;

import dev.federicocalo.managementeconomy.dto.request.RevenueStreamRequest;
import dev.federicocalo.managementeconomy.dto.response.RevenueStreamResponse;
import dev.federicocalo.managementeconomy.enums.RevenueType;
import dev.federicocalo.managementeconomy.service.RevenueService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * REST Controller per la gestione dei revenue streams
 */
@RestController
@RequestMapping("/api/v1/revenues")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*")
public class RevenueController {

    private final RevenueService revenueService;

    /**
     * POST /api/v1/revenues - Crea un nuovo revenue stream
     */
    @PostMapping
    public ResponseEntity<RevenueStreamResponse> create(@Valid @RequestBody RevenueStreamRequest request) {
        log.info("REST: Creating revenue stream: {}", request.getName());
        RevenueStreamResponse response = revenueService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    /**
     * PUT /api/v1/revenues/{id} - Aggiorna un revenue stream
     */
    @PutMapping("/{id}")
    public ResponseEntity<RevenueStreamResponse> update(
            @PathVariable Long id,
            @Valid @RequestBody RevenueStreamRequest request) {
        log.info("REST: Updating revenue stream with id: {}", id);
        RevenueStreamResponse response = revenueService.update(id, request);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/revenues/{id} - Ottiene un revenue stream per ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<RevenueStreamResponse> getById(@PathVariable Long id) {
        log.info("REST: Getting revenue stream with id: {}", id);
        RevenueStreamResponse response = revenueService.findById(id);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/revenues/project/{projectId} - Ottiene tutti i revenue streams di un progetto
     */
    @GetMapping("/project/{projectId}")
    public ResponseEntity<List<RevenueStreamResponse>> getByProject(@PathVariable Long projectId) {
        log.info("REST: Getting all revenue streams for project: {}", projectId);
        List<RevenueStreamResponse> response = revenueService.findByProject(projectId);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/revenues/project/{projectId}/type/{type} - Ottiene revenue streams per tipo
     */
    @GetMapping("/project/{projectId}/type/{type}")
    public ResponseEntity<List<RevenueStreamResponse>> getByProjectAndType(
            @PathVariable Long projectId,
            @PathVariable RevenueType type) {
        log.info("REST: Getting revenue streams for project {} and type {}", projectId, type);
        List<RevenueStreamResponse> response = revenueService.findByProjectAndType(projectId, type);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/revenues/project/{projectId}/date-range - Ottiene revenue streams per range di date
     */
    @GetMapping("/project/{projectId}/date-range")
    public ResponseEntity<List<RevenueStreamResponse>> getByDateRange(
            @PathVariable Long projectId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        log.info("REST: Getting revenue streams for project {} between {} and {}", projectId, startDate, endDate);
        List<RevenueStreamResponse> response = revenueService.findByDateRange(projectId, startDate, endDate);
        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/v1/revenues/project/{projectId}/total - Calcola totale revenue per range di date
     */
    @GetMapping("/project/{projectId}/total")
    public ResponseEntity<Map<String, BigDecimal>> getTotalByDateRange(
            @PathVariable Long projectId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        log.info("REST: Calculating total revenue for project {} between {} and {}", projectId, startDate, endDate);
        BigDecimal total = revenueService.calculateTotalByDateRange(projectId, startDate, endDate);
        return ResponseEntity.ok(Map.of("total", total));
    }

    /**
     * GET /api/v1/revenues/project/{projectId}/totals-by-type - Calcola totali per tipo
     */
    @GetMapping("/project/{projectId}/totals-by-type")
    public ResponseEntity<Map<String, BigDecimal>> getTotalsByType(@PathVariable Long projectId) {
        log.info("REST: Calculating revenue totals by type for project: {}", projectId);
        List<Object[]> results = revenueService.calculateTotalByType(projectId);

        Map<String, BigDecimal> totals = new HashMap<>();
        for (Object[] result : results) {
            RevenueType type = (RevenueType) result[0];
            BigDecimal amount = (BigDecimal) result[1];
            totals.put(type.name(), amount);
        }

        return ResponseEntity.ok(totals);
    }

    /**
     * GET /api/v1/revenues/project/{projectId}/totals-by-source - Calcola totali per source
     */
    @GetMapping("/project/{projectId}/totals-by-source")
    public ResponseEntity<Map<String, BigDecimal>> getTotalsBySource(@PathVariable Long projectId) {
        log.info("REST: Calculating revenue totals by source for project: {}", projectId);
        List<Object[]> results = revenueService.calculateTotalBySource(projectId);

        Map<String, BigDecimal> totals = new HashMap<>();
        for (Object[] result : results) {
            String source = (String) result[0];
            BigDecimal amount = (BigDecimal) result[1];
            totals.put(source, amount);
        }

        return ResponseEntity.ok(totals);
    }

    /**
     * GET /api/v1/revenues/project/{projectId}/monthly - Calcola revenue mensili
     */
    @GetMapping("/project/{projectId}/monthly")
    public ResponseEntity<List<Map<String, Object>>> getMonthlyRevenue(@PathVariable Long projectId) {
        log.info("REST: Calculating monthly revenue for project: {}", projectId);
        List<Object[]> results = revenueService.calculateMonthlyRevenue(projectId);

        List<Map<String, Object>> monthlyData = results.stream()
                .map(result -> {
                    Map<String, Object> monthData = new HashMap<>();
                    monthData.put("year", result[0]);
                    monthData.put("month", result[1]);
                    monthData.put("total", result[2]);
                    return monthData;
                })
                .toList();

        return ResponseEntity.ok(monthlyData);
    }

    /**
     * DELETE /api/v1/revenues/{id} - Elimina un revenue stream
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        log.info("REST: Deleting revenue stream with id: {}", id);
        revenueService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
