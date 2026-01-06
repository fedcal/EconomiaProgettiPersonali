package dev.federicocalo.managementeconomy.controller;

import dev.federicocalo.managementeconomy.dto.TaskRequest;
import dev.federicocalo.managementeconomy.dto.TaskResponse;
import dev.federicocalo.managementeconomy.enums.TaskStatus;
import dev.federicocalo.managementeconomy.service.TaskService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST Controller for Task operations.
 */
@RestController
@RequestMapping("/api/v1/tasks")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*")
public class TaskController {

    private final TaskService taskService;

    /**
     * Get all tasks
     *
     * @return list of all tasks
     */
    @GetMapping
    public ResponseEntity<List<TaskResponse>> getAllTasks() {
        log.info("REST request to get all tasks");
        return ResponseEntity.ok(taskService.findAll());
    }

    /**
     * Get task by ID
     *
     * @param id the task ID
     * @return task response
     */
    @GetMapping("/{id}")
    public ResponseEntity<TaskResponse> getTaskById(@PathVariable Long id) {
        log.info("REST request to get task by id: {}", id);
        return ResponseEntity.ok(taskService.findById(id));
    }

    /**
     * Get all tasks for a specific project
     *
     * @param projectId the project ID
     * @return list of tasks
     */
    @GetMapping("/project/{projectId}")
    public ResponseEntity<List<TaskResponse>> getTasksByProject(@PathVariable Long projectId) {
        log.info("REST request to get tasks for project: {}", projectId);
        return ResponseEntity.ok(taskService.findByProjectId(projectId));
    }

    /**
     * Get tasks by project and status
     *
     * @param projectId the project ID
     * @param status the task status
     * @return list of tasks
     */
    @GetMapping("/project/{projectId}/status/{status}")
    public ResponseEntity<List<TaskResponse>> getTasksByProjectAndStatus(
            @PathVariable Long projectId,
            @PathVariable TaskStatus status) {
        log.info("REST request to get tasks for project {} with status {}", projectId, status);
        return ResponseEntity.ok(taskService.findByProjectIdAndStatus(projectId, status));
    }

    /**
     * Get tasks by project and tag
     *
     * @param projectId the project ID
     * @param tag the tag
     * @return list of tasks
     */
    @GetMapping("/project/{projectId}/tag/{tag}")
    public ResponseEntity<List<TaskResponse>> getTasksByProjectAndTag(
            @PathVariable Long projectId,
            @PathVariable String tag) {
        log.info("REST request to get tasks for project {} with tag {}", projectId, tag);
        return ResponseEntity.ok(taskService.findByProjectIdAndTag(projectId, tag));
    }

    /**
     * Get all tasks with a specific status
     *
     * @param status the task status
     * @return list of tasks
     */
    @GetMapping("/status/{status}")
    public ResponseEntity<List<TaskResponse>> getTasksByStatus(@PathVariable TaskStatus status) {
        log.info("REST request to get tasks with status {}", status);
        return ResponseEntity.ok(taskService.findByStatus(status));
    }

    /**
     * Get all distinct tags for a project
     *
     * @param projectId the project ID
     * @return list of unique tags
     */
    @GetMapping("/project/{projectId}/tags")
    public ResponseEntity<List<String>> getDistinctTags(@PathVariable Long projectId) {
        log.info("REST request to get distinct tags for project: {}", projectId);
        return ResponseEntity.ok(taskService.findDistinctTags(projectId));
    }

    /**
     * Count tasks by project and status
     *
     * @param projectId the project ID
     * @param status the task status
     * @return count of tasks
     */
    @GetMapping("/project/{projectId}/status/{status}/count")
    public ResponseEntity<Long> countTasksByProjectAndStatus(
            @PathVariable Long projectId,
            @PathVariable TaskStatus status) {
        log.info("REST request to count tasks for project {} with status {}", projectId, status);
        return ResponseEntity.ok(taskService.countByProjectIdAndStatus(projectId, status));
    }

    /**
     * Count total tasks for a project
     *
     * @param projectId the project ID
     * @return count of tasks
     */
    @GetMapping("/project/{projectId}/count")
    public ResponseEntity<Long> countTasksByProject(@PathVariable Long projectId) {
        log.info("REST request to count tasks for project: {}", projectId);
        return ResponseEntity.ok(taskService.countByProjectId(projectId));
    }

    /**
     * Create a new task
     *
     * @param request the task request
     * @return created task response
     */
    @PostMapping
    public ResponseEntity<TaskResponse> createTask(@Valid @RequestBody TaskRequest request) {
        log.info("REST request to create task: {}", request);
        TaskResponse response = taskService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    /**
     * Update an existing task
     *
     * @param id the task ID
     * @param request the task request
     * @return updated task response
     */
    @PutMapping("/{id}")
    public ResponseEntity<TaskResponse> updateTask(
            @PathVariable Long id,
            @Valid @RequestBody TaskRequest request) {
        log.info("REST request to update task {}: {}", id, request);
        return ResponseEntity.ok(taskService.update(id, request));
    }

    /**
     * Delete a task
     *
     * @param id the task ID
     * @return no content
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteTask(@PathVariable Long id) {
        log.info("REST request to delete task: {}", id);
        taskService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
