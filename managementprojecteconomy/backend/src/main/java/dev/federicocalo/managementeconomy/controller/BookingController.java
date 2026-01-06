package dev.federicocalo.managementeconomy.controller;

import dev.federicocalo.managementeconomy.dto.request.BookingCreateRequest;
import dev.federicocalo.managementeconomy.dto.request.BookingUpdateRequest;
import dev.federicocalo.managementeconomy.dto.response.BookingResponse;
import dev.federicocalo.managementeconomy.enums.BookingStatus;
import dev.federicocalo.managementeconomy.service.BookingService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

/**
 * REST Controller per gestione prenotazioni
 * Base path: /api/v1/bookings
 */
@RestController
@RequestMapping("/api/v1/bookings")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "${cors.allowed-origins}")
public class BookingController {

    private final BookingService bookingService;

    /**
     * GET /api/v1/bookings/{id}
     * Ottiene prenotazione per ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<BookingResponse> getBookingById(@PathVariable Long id) {
        log.info("GET /api/v1/bookings/{} - Fetching booking by id", id);
        BookingResponse booking = bookingService.findById(id);
        return ResponseEntity.ok(booking);
    }

    /**
     * GET /api/v1/bookings/project/{projectId}
     * Ottiene tutte le prenotazioni di un progetto
     */
    @GetMapping("/project/{projectId}")
    public ResponseEntity<List<BookingResponse>> getBookingsByProject(@PathVariable Long projectId) {
        log.info("GET /api/v1/bookings/project/{} - Fetching bookings by project", projectId);
        List<BookingResponse> bookings = bookingService.findByProjectId(projectId);
        return ResponseEntity.ok(bookings);
    }

    /**
     * GET /api/v1/bookings/project/{projectId}/status/{status}
     * Ottiene prenotazioni per progetto e stato
     */
    @GetMapping("/project/{projectId}/status/{status}")
    public ResponseEntity<List<BookingResponse>> getBookingsByProjectAndStatus(
            @PathVariable Long projectId,
            @PathVariable BookingStatus status) {
        log.info("GET /api/v1/bookings/project/{}/status/{} - Fetching bookings by project and status",
            projectId, status);
        List<BookingResponse> bookings = bookingService.findByProjectIdAndStatus(projectId, status);
        return ResponseEntity.ok(bookings);
    }

    /**
     * GET /api/v1/bookings/project/{projectId}/date-range
     * Ottiene prenotazioni per progetto e range di date
     */
    @GetMapping("/project/{projectId}/date-range")
    public ResponseEntity<List<BookingResponse>> getBookingsByDateRange(
            @PathVariable Long projectId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate) {
        log.info("GET /api/v1/bookings/project/{}/date-range - Fetching bookings from {} to {}",
            projectId, startDate, endDate);
        List<BookingResponse> bookings = bookingService.findByDateRange(projectId, startDate, endDate);
        return ResponseEntity.ok(bookings);
    }

    /**
     * GET /api/v1/bookings/project/{projectId}/year/{year}
     * Ottiene prenotazioni per progetto e anno
     */
    @GetMapping("/project/{projectId}/year/{year}")
    public ResponseEntity<List<BookingResponse>> getBookingsByYear(
            @PathVariable Long projectId,
            @PathVariable int year) {
        log.info("GET /api/v1/bookings/project/{}/year/{} - Fetching bookings by year", projectId, year);
        List<BookingResponse> bookings = bookingService.findByYear(projectId, year);
        return ResponseEntity.ok(bookings);
    }

    /**
     * GET /api/v1/bookings/project/{projectId}/platform/{platform}
     * Ottiene prenotazioni per progetto e piattaforma
     */
    @GetMapping("/project/{projectId}/platform/{platform}")
    public ResponseEntity<List<BookingResponse>> getBookingsByPlatform(
            @PathVariable Long projectId,
            @PathVariable String platform) {
        log.info("GET /api/v1/bookings/project/{}/platform/{} - Fetching bookings by platform",
            projectId, platform);
        List<BookingResponse> bookings = bookingService.findByPlatform(projectId, platform);
        return ResponseEntity.ok(bookings);
    }

    /**
     * POST /api/v1/bookings
     * Crea una nuova prenotazione
     */
    @PostMapping
    public ResponseEntity<BookingResponse> createBooking(@Valid @RequestBody BookingCreateRequest request) {
        log.info("POST /api/v1/bookings - Creating new booking for project {}", request.getProjectId());
        BookingResponse created = bookingService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    /**
     * PUT /api/v1/bookings/{id}
     * Aggiorna prenotazione esistente
     */
    @PutMapping("/{id}")
    public ResponseEntity<BookingResponse> updateBooking(
            @PathVariable Long id,
            @Valid @RequestBody BookingUpdateRequest request) {
        log.info("PUT /api/v1/bookings/{} - Updating booking", id);
        BookingResponse updated = bookingService.update(id, request);
        return ResponseEntity.ok(updated);
    }

    /**
     * PATCH /api/v1/bookings/{id}/status
     * Cambia stato prenotazione
     */
    @PatchMapping("/{id}/status")
    public ResponseEntity<BookingResponse> changeBookingStatus(
            @PathVariable Long id,
            @RequestParam BookingStatus status) {
        log.info("PATCH /api/v1/bookings/{}/status - Changing status to {}", id, status);
        BookingResponse updated = bookingService.changeStatus(id, status);
        return ResponseEntity.ok(updated);
    }

    /**
     * PATCH /api/v1/bookings/{id}/cancel
     * Cancella prenotazione
     */
    @PatchMapping("/{id}/cancel")
    public ResponseEntity<BookingResponse> cancelBooking(@PathVariable Long id) {
        log.info("PATCH /api/v1/bookings/{}/cancel - Cancelling booking", id);
        BookingResponse cancelled = bookingService.cancel(id);
        return ResponseEntity.ok(cancelled);
    }

    /**
     * PATCH /api/v1/bookings/{id}/complete
     * Completa prenotazione
     */
    @PatchMapping("/{id}/complete")
    public ResponseEntity<BookingResponse> completeBooking(@PathVariable Long id) {
        log.info("PATCH /api/v1/bookings/{}/complete - Completing booking", id);
        BookingResponse completed = bookingService.complete(id);
        return ResponseEntity.ok(completed);
    }

    /**
     * DELETE /api/v1/bookings/{id}
     * Elimina prenotazione
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteBooking(@PathVariable Long id) {
        log.info("DELETE /api/v1/bookings/{} - Deleting booking", id);
        bookingService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
