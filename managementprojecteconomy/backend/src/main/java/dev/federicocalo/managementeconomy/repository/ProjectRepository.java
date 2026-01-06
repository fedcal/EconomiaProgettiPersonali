package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.Project;
import dev.federicocalo.managementeconomy.enums.ProjectStatus;
import dev.federicocalo.managementeconomy.enums.ProjectType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Repository per gestione progetti
 */
@Repository
public interface ProjectRepository extends JpaRepository<Project, Long> {

    /**
     * Trova progetto per codice univoco
     */
    Optional<Project> findByCode(String code);

    /**
     * Trova tutti i progetti per stato
     */
    List<Project> findByStatus(ProjectStatus status);

    /**
     * Trova tutti i progetti per tipo
     */
    List<Project> findByType(ProjectType type);

    /**
     * Verifica se esiste un progetto con il codice specificato
     */
    boolean existsByCode(String code);

    /**
     * Verifica se esiste un progetto con il nome specificato
     */
    boolean existsByName(String name);

    /**
     * Trova progetti attivi ordinati per data inizio
     */
    @Query("SELECT p FROM Project p WHERE p.status = :status ORDER BY p.startDate DESC")
    List<Project> findActiveProjects(@Param("status") ProjectStatus status);

    /**
     * Conta progetti per tipo
     */
    long countByType(ProjectType type);

    /**
     * Trova progetti per tipo e stato
     */
    List<Project> findByTypeAndStatus(ProjectType type, ProjectStatus status);
}
