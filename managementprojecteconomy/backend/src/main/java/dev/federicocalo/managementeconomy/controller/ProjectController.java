package dev.federicocalo.managementeconomy.controller;

import dev.federicocalo.managementeconomy.dto.request.ProjectCreateRequest;
import dev.federicocalo.managementeconomy.dto.request.ProjectUpdateRequest;
import dev.federicocalo.managementeconomy.dto.response.ProjectResponse;
import dev.federicocalo.managementeconomy.enums.ProjectStatus;
import dev.federicocalo.managementeconomy.enums.ProjectType;
import dev.federicocalo.managementeconomy.service.ProjectService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST Controller per gestione progetti
 * Base path: /api/v1/projects
 */
@RestController
@RequestMapping("/api/v1/projects")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "${cors.allowed-origins}")
public class ProjectController {

    private final ProjectService projectService;

    /**
     * GET /api/v1/projects
     * Ottiene tutti i progetti
     */
    @GetMapping
    public ResponseEntity<List<ProjectResponse>> getAllProjects() {
        log.info("GET /api/v1/projects - Fetching all projects");
        List<ProjectResponse> projects = projectService.findAll();
        return ResponseEntity.ok(projects);
    }

    /**
     * GET /api/v1/projects/{id}
     * Ottiene progetto per ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<ProjectResponse> getProjectById(@PathVariable Long id) {
        log.info("GET /api/v1/projects/{} - Fetching project by id", id);
        ProjectResponse project = projectService.findById(id);
        return ResponseEntity.ok(project);
    }

    /**
     * GET /api/v1/projects/code/{code}
     * Ottiene progetto per codice
     */
    @GetMapping("/code/{code}")
    public ResponseEntity<ProjectResponse> getProjectByCode(@PathVariable String code) {
        log.info("GET /api/v1/projects/code/{} - Fetching project by code", code);
        ProjectResponse project = projectService.findByCode(code);
        return ResponseEntity.ok(project);
    }

    /**
     * GET /api/v1/projects/status/{status}
     * Ottiene progetti per stato
     */
    @GetMapping("/status/{status}")
    public ResponseEntity<List<ProjectResponse>> getProjectsByStatus(@PathVariable ProjectStatus status) {
        log.info("GET /api/v1/projects/status/{} - Fetching projects by status", status);
        List<ProjectResponse> projects = projectService.findByStatus(status);
        return ResponseEntity.ok(projects);
    }

    /**
     * GET /api/v1/projects/type/{type}
     * Ottiene progetti per tipo
     */
    @GetMapping("/type/{type}")
    public ResponseEntity<List<ProjectResponse>> getProjectsByType(@PathVariable ProjectType type) {
        log.info("GET /api/v1/projects/type/{} - Fetching projects by type", type);
        List<ProjectResponse> projects = projectService.findByType(type);
        return ResponseEntity.ok(projects);
    }

    /**
     * GET /api/v1/projects/active
     * Ottiene solo progetti attivi
     */
    @GetMapping("/active")
    public ResponseEntity<List<ProjectResponse>> getActiveProjects() {
        log.info("GET /api/v1/projects/active - Fetching active projects");
        List<ProjectResponse> projects = projectService.findActiveProjects();
        return ResponseEntity.ok(projects);
    }

    /**
     * POST /api/v1/projects
     * Crea un nuovo progetto
     */
    @PostMapping
    public ResponseEntity<ProjectResponse> createProject(@Valid @RequestBody ProjectCreateRequest request) {
        log.info("POST /api/v1/projects - Creating new project: {}", request.getCode());
        ProjectResponse created = projectService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    /**
     * PUT /api/v1/projects/{id}
     * Aggiorna progetto esistente
     */
    @PutMapping("/{id}")
    public ResponseEntity<ProjectResponse> updateProject(
            @PathVariable Long id,
            @Valid @RequestBody ProjectUpdateRequest request) {
        log.info("PUT /api/v1/projects/{} - Updating project", id);
        ProjectResponse updated = projectService.update(id, request);
        return ResponseEntity.ok(updated);
    }

    /**
     * PATCH /api/v1/projects/{id}/status
     * Cambia stato progetto
     */
    @PatchMapping("/{id}/status")
    public ResponseEntity<ProjectResponse> changeProjectStatus(
            @PathVariable Long id,
            @RequestParam ProjectStatus status) {
        log.info("PATCH /api/v1/projects/{}/status - Changing status to {}", id, status);
        ProjectResponse updated = projectService.changeStatus(id, status);
        return ResponseEntity.ok(updated);
    }

    /**
     * PATCH /api/v1/projects/{id}/archive
     * Archivia progetto
     */
    @PatchMapping("/{id}/archive")
    public ResponseEntity<ProjectResponse> archiveProject(@PathVariable Long id) {
        log.info("PATCH /api/v1/projects/{}/archive - Archiving project", id);
        ProjectResponse archived = projectService.archive(id);
        return ResponseEntity.ok(archived);
    }

    /**
     * DELETE /api/v1/projects/{id}
     * Elimina progetto
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProject(@PathVariable Long id) {
        log.info("DELETE /api/v1/projects/{} - Deleting project", id);
        projectService.delete(id);
        return ResponseEntity.noContent().build();
    }

    /**
     * GET /api/v1/projects/count/type/{type}
     * Conta progetti per tipo
     */
    @GetMapping("/count/type/{type}")
    public ResponseEntity<Long> countProjectsByType(@PathVariable ProjectType type) {
        log.info("GET /api/v1/projects/count/type/{} - Counting projects by type", type);
        long count = projectService.countByType(type);
        return ResponseEntity.ok(count);
    }
}
