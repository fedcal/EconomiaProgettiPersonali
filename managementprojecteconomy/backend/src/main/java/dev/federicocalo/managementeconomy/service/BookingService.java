package dev.federicocalo.managementeconomy.service;

import dev.federicocalo.managementeconomy.dto.mapper.BookingMapper;
import dev.federicocalo.managementeconomy.dto.request.BookingCreateRequest;
import dev.federicocalo.managementeconomy.dto.request.BookingUpdateRequest;
import dev.federicocalo.managementeconomy.dto.response.BookingResponse;
import dev.federicocalo.managementeconomy.entity.Booking;
import dev.federicocalo.managementeconomy.entity.PlatformCommission;
import dev.federicocalo.managementeconomy.entity.Project;
import dev.federicocalo.managementeconomy.enums.BookingStatus;
import dev.federicocalo.managementeconomy.exception.DuplicateResourceException;
import dev.federicocalo.managementeconomy.exception.InvalidDataException;
import dev.federicocalo.managementeconomy.exception.ResourceNotFoundException;
import dev.federicocalo.managementeconomy.repository.BookingRepository;
import dev.federicocalo.managementeconomy.repository.PlatformCommissionRepository;
import dev.federicocalo.managementeconomy.repository.ProjectRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.util.List;

/**
 * Service per gestione prenotazioni con auto-calcolo commissioni
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class BookingService {

    private final BookingRepository bookingRepository;
    private final ProjectRepository projectRepository;
    private final PlatformCommissionRepository platformCommissionRepository;
    private final BookingMapper bookingMapper;

    private static final BigDecimal DEFAULT_COMMISSION_RATE = BigDecimal.valueOf(15.00);

    /**
     * Crea una nuova prenotazione con auto-calcolo commissioni
     */
    public BookingResponse create(BookingCreateRequest request) {
        log.info("Creating new booking for project {}, platform: {}",
            request.getProjectId(), request.getPlatform());

        // Verifica che il progetto esista
        Project project = projectRepository.findById(request.getProjectId())
            .orElseThrow(() -> new ResourceNotFoundException(
                "Progetto con id " + request.getProjectId() + " non trovato"));

        // Verifica sovrapposizioni date
        if (bookingRepository.existsOverlappingBooking(
                request.getProjectId(),
                request.getCheckinDate(),
                request.getCheckoutDate())) {
            throw new DuplicateResourceException(
                "Esiste già una prenotazione sovrapposta per queste date");
        }

        // Crea entity
        Booking booking = bookingMapper.toEntity(request);
        booking.setProject(project);

        // Auto-calcola commissione dalla piattaforma
        BigDecimal commissionRate = getCommissionRateForPlatform(request.getPlatform());
        BigDecimal commissionAmount = request.getPrice()
            .multiply(commissionRate)
            .divide(BigDecimal.valueOf(100), 2, RoundingMode.HALF_UP);

        booking.setCommissionRate(commissionRate);
        booking.setCommissionAmount(commissionAmount);

        // Il @PrePersist calcolerà nights, pricePerNight e netRevenue
        Booking saved = bookingRepository.save(booking);

        log.info("Booking created successfully with id: {}, commission: €{}",
            saved.getId(), saved.getCommissionAmount());
        return bookingMapper.toResponse(saved);
    }

    /**
     * Trova prenotazione per ID
     */
    @Transactional(readOnly = true)
    public BookingResponse findById(Long id) {
        log.debug("Finding booking by id: {}", id);
        Booking booking = getBookingOrThrow(id);
        return bookingMapper.toResponse(booking);
    }

    /**
     * Trova tutte le prenotazioni di un progetto
     */
    @Transactional(readOnly = true)
    public List<BookingResponse> findByProjectId(Long projectId) {
        log.debug("Finding bookings for project: {}", projectId);
        List<Booking> bookings = bookingRepository.findByProjectId(projectId);
        return bookingMapper.toResponseList(bookings);
    }

    /**
     * Trova prenotazioni per progetto e stato
     */
    @Transactional(readOnly = true)
    public List<BookingResponse> findByProjectIdAndStatus(Long projectId, BookingStatus status) {
        log.debug("Finding bookings for project {} with status {}", projectId, status);
        List<Booking> bookings = bookingRepository.findByProjectIdAndBookingStatus(projectId, status);
        return bookingMapper.toResponseList(bookings);
    }

    /**
     * Trova prenotazioni per range di date
     */
    @Transactional(readOnly = true)
    public List<BookingResponse> findByDateRange(Long projectId, LocalDate startDate, LocalDate endDate) {
        log.debug("Finding bookings for project {} between {} and {}", projectId, startDate, endDate);
        List<Booking> bookings = bookingRepository.findByProjectIdAndDateRange(projectId, startDate, endDate);
        return bookingMapper.toResponseList(bookings);
    }

    /**
     * Trova prenotazioni per anno
     */
    @Transactional(readOnly = true)
    public List<BookingResponse> findByYear(Long projectId, int year) {
        log.debug("Finding bookings for project {} in year {}", projectId, year);
        List<Booking> bookings = bookingRepository.findByProjectIdAndYear(projectId, year);
        return bookingMapper.toResponseList(bookings);
    }

    /**
     * Trova prenotazioni per piattaforma
     */
    @Transactional(readOnly = true)
    public List<BookingResponse> findByPlatform(Long projectId, String platform) {
        log.debug("Finding bookings for project {} on platform {}", projectId, platform);
        List<Booking> bookings = bookingRepository.findByProjectIdAndPlatform(projectId, platform);
        return bookingMapper.toResponseList(bookings);
    }

    /**
     * Aggiorna prenotazione esistente
     */
    public BookingResponse update(Long id, BookingUpdateRequest request) {
        log.info("Updating booking with id: {}", id);

        Booking booking = getBookingOrThrow(id);

        // Verifica sovrapposizioni (escludi la prenotazione corrente)
        if (!booking.getCheckinDate().equals(request.getCheckinDate()) ||
            !booking.getCheckoutDate().equals(request.getCheckoutDate())) {

            if (bookingRepository.existsOverlappingBooking(
                    booking.getProject().getId(),
                    request.getCheckinDate(),
                    request.getCheckoutDate())) {
                throw new DuplicateResourceException(
                    "Esiste già una prenotazione sovrapposta per queste date");
            }
        }

        // Ricalcola commissione se piattaforma o prezzo cambiano
        if (!booking.getPlatform().equals(request.getPlatform()) ||
            !booking.getPrice().equals(request.getPrice())) {

            BigDecimal commissionRate = getCommissionRateForPlatform(request.getPlatform());
            BigDecimal commissionAmount = request.getPrice()
                .multiply(commissionRate)
                .divide(BigDecimal.valueOf(100), 2, RoundingMode.HALF_UP);

            booking.setCommissionRate(commissionRate);
            booking.setCommissionAmount(commissionAmount);
        }

        bookingMapper.updateEntityFromRequest(request, booking);
        Booking updated = bookingRepository.save(booking);

        log.info("Booking updated successfully");
        return bookingMapper.toResponse(updated);
    }

    /**
     * Cambia stato prenotazione
     */
    public BookingResponse changeStatus(Long id, BookingStatus newStatus) {
        log.info("Changing status of booking {} to {}", id, newStatus);

        Booking booking = getBookingOrThrow(id);
        booking.setBookingStatus(newStatus);
        Booking updated = bookingRepository.save(booking);

        return bookingMapper.toResponse(updated);
    }

    /**
     * Cancella prenotazione
     */
    public BookingResponse cancel(Long id) {
        return changeStatus(id, BookingStatus.CANCELLED);
    }

    /**
     * Completa prenotazione
     */
    public BookingResponse complete(Long id) {
        return changeStatus(id, BookingStatus.COMPLETED);
    }

    /**
     * Elimina prenotazione
     */
    public void delete(Long id) {
        log.info("Deleting booking with id: {}", id);

        if (!bookingRepository.existsById(id)) {
            throw new ResourceNotFoundException("Prenotazione con id " + id + " non trovata");
        }

        bookingRepository.deleteById(id);
        log.info("Booking deleted successfully");
    }

    /**
     * Ottiene commission rate per piattaforma dal database
     */
    private BigDecimal getCommissionRateForPlatform(String platform) {
        return platformCommissionRepository.findByPlatformNameIgnoreCase(platform)
            .map(PlatformCommission::getCommissionRate)
            .orElseGet(() -> {
                log.warn("Commission rate not found for platform {}, using default {}%",
                    platform, DEFAULT_COMMISSION_RATE);
                return DEFAULT_COMMISSION_RATE;
            });
    }

    /**
     * Helper method - ottieni prenotazione o lancia eccezione
     */
    private Booking getBookingOrThrow(Long id) {
        return bookingRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException(
                "Prenotazione con id " + id + " non trovata"));
    }
}
