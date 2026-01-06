package dev.federicocalo.managementeconomy.service;

import dev.federicocalo.managementeconomy.dto.request.SubscriptionRequest;
import dev.federicocalo.managementeconomy.dto.response.SubscriptionResponse;
import dev.federicocalo.managementeconomy.entity.Project;
import dev.federicocalo.managementeconomy.entity.Subscription;
import dev.federicocalo.managementeconomy.enums.SubscriptionStatus;
import dev.federicocalo.managementeconomy.exception.ResourceNotFoundException;
import dev.federicocalo.managementeconomy.mapper.SubscriptionMapper;
import dev.federicocalo.managementeconomy.repository.ProjectRepository;
import dev.federicocalo.managementeconomy.repository.SubscriptionRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service per la gestione delle subscriptions (SaaS)
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class SubscriptionService {

    private final SubscriptionRepository subscriptionRepository;
    private final ProjectRepository projectRepository;
    private final SubscriptionMapper subscriptionMapper;

    /**
     * Crea una nuova subscription
     */
    public SubscriptionResponse create(SubscriptionRequest request) {
        log.info("Creating subscription for customer: {} in project {}", request.getCustomerName(), request.getProjectId());

        Project project = projectRepository.findById(request.getProjectId())
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));

        Subscription subscription = subscriptionMapper.toEntity(request);
        subscription.setProject(project);

        Subscription savedSubscription = subscriptionRepository.save(subscription);
        log.info("Subscription created successfully with id: {}", savedSubscription.getId());

        return subscriptionMapper.toResponse(savedSubscription);
    }

    /**
     * Aggiorna una subscription esistente
     */
    public SubscriptionResponse update(Long id, SubscriptionRequest request) {
        log.info("Updating subscription with id: {}", id);

        Subscription existingSubscription = subscriptionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Subscription", "id", id));

        // Se il projectId è cambiato, verifica che esista
        if (!existingSubscription.getProject().getId().equals(request.getProjectId())) {
            Project newProject = projectRepository.findById(request.getProjectId())
                    .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));
            existingSubscription.setProject(newProject);
        }

        subscriptionMapper.updateEntityFromRequest(request, existingSubscription);
        Subscription updatedSubscription = subscriptionRepository.save(existingSubscription);

        log.info("Subscription updated successfully");
        return subscriptionMapper.toResponse(updatedSubscription);
    }

    /**
     * Trova una subscription per ID
     */
    @Transactional(readOnly = true)
    public SubscriptionResponse findById(Long id) {
        log.debug("Finding subscription with id: {}", id);

        Subscription subscription = subscriptionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Subscription", "id", id));

        return subscriptionMapper.toResponse(subscription);
    }

    /**
     * Trova tutte le subscriptions di un progetto
     */
    @Transactional(readOnly = true)
    public List<SubscriptionResponse> findByProject(Long projectId) {
        log.debug("Finding all subscriptions for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        List<Subscription> subscriptions = subscriptionRepository.findByProjectId(projectId);
        return subscriptions.stream()
                .map(subscriptionMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Trova subscriptions attive per un progetto
     */
    @Transactional(readOnly = true)
    public List<SubscriptionResponse> findActiveSubscriptions(Long projectId) {
        log.debug("Finding active subscriptions for project: {}", projectId);

        List<Subscription> subscriptions = subscriptionRepository.findActiveByProjectId(projectId);
        return subscriptions.stream()
                .map(subscriptionMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Calcola il totale MRR per un progetto
     */
    @Transactional(readOnly = true)
    public BigDecimal calculateTotalMRR(Long projectId) {
        log.debug("Calculating total MRR for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return subscriptionRepository.calculateTotalMRR(projectId);
    }

    /**
     * Conta le subscriptions attive
     */
    @Transactional(readOnly = true)
    public long countActiveSubscriptions(Long projectId) {
        log.debug("Counting active subscriptions for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return subscriptionRepository.countActiveSubscriptions(projectId);
    }

    /**
     * Conta subscriptions per piano
     */
    @Transactional(readOnly = true)
    public List<Object[]> countSubscriptionsByPlan(Long projectId) {
        log.debug("Counting subscriptions by plan for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return subscriptionRepository.countSubscriptionsByPlan(projectId);
    }

    /**
     * Calcola MRR per piano
     */
    @Transactional(readOnly = true)
    public List<Object[]> calculateMRRByPlan(Long projectId) {
        log.debug("Calculating MRR by plan for project: {}", projectId);

        // Verifica che il progetto esista
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return subscriptionRepository.calculateMRRByPlan(projectId);
    }

    /**
     * Cancella una subscription (cambia stato a CANCELLED)
     */
    public SubscriptionResponse cancel(Long id) {
        log.info("Cancelling subscription with id: {}", id);

        Subscription subscription = subscriptionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Subscription", "id", id));

        subscription.setSubscriptionStatus(SubscriptionStatus.CANCELLED);
        Subscription updatedSubscription = subscriptionRepository.save(subscription);

        log.info("Subscription cancelled successfully");
        return subscriptionMapper.toResponse(updatedSubscription);
    }

    /**
     * Riattiva una subscription
     */
    public SubscriptionResponse reactivate(Long id) {
        log.info("Reactivating subscription with id: {}", id);

        Subscription subscription = subscriptionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Subscription", "id", id));

        subscription.setSubscriptionStatus(SubscriptionStatus.ACTIVE);
        Subscription updatedSubscription = subscriptionRepository.save(subscription);

        log.info("Subscription reactivated successfully");
        return subscriptionMapper.toResponse(updatedSubscription);
    }

    /**
     * Elimina una subscription
     */
    public void delete(Long id) {
        log.info("Deleting subscription with id: {}", id);

        if (!subscriptionRepository.existsById(id)) {
            throw new ResourceNotFoundException("Subscription", "id", id);
        }

        subscriptionRepository.deleteById(id);
        log.info("Subscription deleted successfully");
    }
}
