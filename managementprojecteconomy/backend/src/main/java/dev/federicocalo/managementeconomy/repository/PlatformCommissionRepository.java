package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.PlatformCommission;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Repository per gestione commissioni piattaforme
 */
@Repository
public interface PlatformCommissionRepository extends JpaRepository<PlatformCommission, Long> {

    /**
     * Trova commissione per nome piattaforma
     */
    Optional<PlatformCommission> findByPlatformName(String platformName);

    /**
     * Trova commissione per nome piattaforma (case insensitive)
     */
    Optional<PlatformCommission> findByPlatformNameIgnoreCase(String platformName);

    /**
     * Trova tutte le piattaforme attive
     */
    List<PlatformCommission> findByIsActiveTrue();

    /**
     * Verifica se esiste una piattaforma con il nome specificato
     */
    boolean existsByPlatformName(String platformName);
}
