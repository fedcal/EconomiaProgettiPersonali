package dev.federicocalo.managementeconomy.service;

import dev.federicocalo.managementeconomy.dto.mapper.ProjectMapper;
import dev.federicocalo.managementeconomy.dto.request.ProjectCreateRequest;
import dev.federicocalo.managementeconomy.dto.request.ProjectUpdateRequest;
import dev.federicocalo.managementeconomy.dto.response.ProjectResponse;
import dev.federicocalo.managementeconomy.entity.Project;
import dev.federicocalo.managementeconomy.enums.ProjectStatus;
import dev.federicocalo.managementeconomy.enums.ProjectType;
import dev.federicocalo.managementeconomy.exception.DuplicateResourceException;
import dev.federicocalo.managementeconomy.exception.ResourceNotFoundException;
import dev.federicocalo.managementeconomy.repository.ProjectRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * Service per gestione progetti
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class ProjectService {

    private final ProjectRepository projectRepository;
    private final ProjectMapper projectMapper;

    /**
     * Crea un nuovo progetto
     */
    public ProjectResponse create(ProjectCreateRequest request) {
        log.info("Creating new project with code: {}", request.getCode());

        // Verifica duplicati
        if (projectRepository.existsByCode(request.getCode())) {
            throw new DuplicateResourceException("Progetto con codice '" + request.getCode() + "' già esistente");
        }
        if (projectRepository.existsByName(request.getName())) {
            throw new DuplicateResourceException("Progetto con nome '" + request.getName() + "' già esistente");
        }

        Project project = projectMapper.toEntity(request);
        Project saved = projectRepository.save(project);

        log.info("Project created successfully with id: {}", saved.getId());
        return projectMapper.toResponse(saved);
    }

    /**
     * Trova progetto per ID
     */
    @Transactional(readOnly = true)
    public ProjectResponse findById(Long id) {
        log.debug("Finding project by id: {}", id);
        Project project = getProjectOrThrow(id);
        return projectMapper.toResponse(project);
    }

    /**
     * Trova progetto per codice
     */
    @Transactional(readOnly = true)
    public ProjectResponse findByCode(String code) {
        log.debug("Finding project by code: {}", code);
        Project project = projectRepository.findByCode(code)
                .orElseThrow(() -> new ResourceNotFoundException("Progetto con codice '" + code + "' non trovato"));
        return projectMapper.toResponse(project);
    }

    /**
     * Trova tutti i progetti
     */
    @Transactional(readOnly = true)
    public List<ProjectResponse> findAll() {
        log.debug("Finding all projects");
        List<Project> projects = projectRepository.findAll();
        return projectMapper.toResponseList(projects);
    }

    /**
     * Trova progetti per stato
     */
    @Transactional(readOnly = true)
    public List<ProjectResponse> findByStatus(ProjectStatus status) {
        log.debug("Finding projects by status: {}", status);
        List<Project> projects = projectRepository.findByStatus(status);
        return projectMapper.toResponseList(projects);
    }

    /**
     * Trova progetti per tipo
     */
    @Transactional(readOnly = true)
    public List<ProjectResponse> findByType(ProjectType type) {
        log.debug("Finding projects by type: {}", type);
        List<Project> projects = projectRepository.findByType(type);
        return projectMapper.toResponseList(projects);
    }

    /**
     * Trova progetti attivi
     */
    @Transactional(readOnly = true)
    public List<ProjectResponse> findActiveProjects() {
        log.debug("Finding active projects");
        List<Project> projects = projectRepository.findActiveProjects(ProjectStatus.ACTIVE);
        return projectMapper.toResponseList(projects);
    }

    /**
     * Aggiorna progetto esistente
     */
    public ProjectResponse update(Long id, ProjectUpdateRequest request) {
        log.info("Updating project with id: {}", id);

        Project project = getProjectOrThrow(id);

        // Verifica duplicato nome (solo se è diverso da quello attuale)
        if (!project.getName().equals(request.getName()) && projectRepository.existsByName(request.getName())) {
            throw new DuplicateResourceException("Progetto con nome '" + request.getName() + "' già esistente");
        }

        projectMapper.updateEntityFromRequest(request, project);
        Project updated = projectRepository.save(project);

        log.info("Project updated successfully with id: {}", id);
        return projectMapper.toResponse(updated);
    }

    /**
     * Cambia stato progetto
     */
    public ProjectResponse changeStatus(Long id, ProjectStatus newStatus) {
        log.info("Changing status of project {} to {}", id, newStatus);

        Project project = getProjectOrThrow(id);
        project.setStatus(newStatus);
        Project updated = projectRepository.save(project);

        log.info("Project status changed successfully");
        return projectMapper.toResponse(updated);
    }

    /**
     * Archivia progetto
     */
    public ProjectResponse archive(Long id) {
        return changeStatus(id, ProjectStatus.ARCHIVED);
    }

    /**
     * Elimina progetto
     */
    public void delete(Long id) {
        log.info("Deleting project with id: {}", id);

        if (!projectRepository.existsById(id)) {
            throw new ResourceNotFoundException("Progetto con id " + id + " non trovato");
        }

        projectRepository.deleteById(id);
        log.info("Project deleted successfully");
    }

    /**
     * Conta progetti per tipo
     */
    @Transactional(readOnly = true)
    public long countByType(ProjectType type) {
        return projectRepository.countByType(type);
    }

    /**
     * Helper method - ottieni progetto o lancia eccezione
     */
    private Project getProjectOrThrow(Long id) {
        return projectRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Progetto con id " + id + " non trovato"));
    }
}
