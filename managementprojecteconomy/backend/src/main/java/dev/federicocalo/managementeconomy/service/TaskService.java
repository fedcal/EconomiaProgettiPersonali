package dev.federicocalo.managementeconomy.service;

import dev.federicocalo.managementeconomy.dto.TaskRequest;
import dev.federicocalo.managementeconomy.dto.TaskResponse;
import dev.federicocalo.managementeconomy.entity.Project;
import dev.federicocalo.managementeconomy.entity.Task;
import dev.federicocalo.managementeconomy.enums.TaskStatus;
import dev.federicocalo.managementeconomy.exception.ResourceNotFoundException;
import dev.federicocalo.managementeconomy.mapper.TaskMapper;
import dev.federicocalo.managementeconomy.repository.ProjectRepository;
import dev.federicocalo.managementeconomy.repository.TaskRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Service layer for Task operations.
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional(readOnly = true)
public class TaskService {

    private final TaskRepository taskRepository;
    private final ProjectRepository projectRepository;
    private final TaskMapper taskMapper;

    /**
     * Get all tasks
     *
     * @return list of all tasks
     */
    public List<TaskResponse> findAll() {
        log.debug("Finding all tasks");
        return taskRepository.findAll().stream()
                .map(taskMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Get task by ID
     *
     * @param id the task ID
     * @return task response
     */
    public TaskResponse findById(Long id) {
        log.debug("Finding task by id: {}", id);
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Task", "id", id));
        return taskMapper.toResponse(task);
    }

    /**
     * Get all tasks for a specific project
     *
     * @param projectId the project ID
     * @return list of tasks
     */
    public List<TaskResponse> findByProjectId(Long projectId) {
        log.debug("Finding tasks for project: {}", projectId);
        // Verify project exists
        projectRepository.findById(projectId)
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", projectId));

        return taskRepository.findByProjectId(projectId).stream()
                .map(taskMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Get tasks by project and status
     *
     * @param projectId the project ID
     * @param status the task status
     * @return list of tasks
     */
    public List<TaskResponse> findByProjectIdAndStatus(Long projectId, TaskStatus status) {
        log.debug("Finding tasks for project {} with status {}", projectId, status);
        return taskRepository.findByProjectIdAndStatus(projectId, status).stream()
                .map(taskMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Get tasks by project and tag
     *
     * @param projectId the project ID
     * @param tag the tag
     * @return list of tasks
     */
    public List<TaskResponse> findByProjectIdAndTag(Long projectId, String tag) {
        log.debug("Finding tasks for project {} with tag {}", projectId, tag);
        return taskRepository.findByProjectIdAndTag(projectId, tag).stream()
                .map(taskMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Get all tasks with a specific status
     *
     * @param status the task status
     * @return list of tasks
     */
    public List<TaskResponse> findByStatus(TaskStatus status) {
        log.debug("Finding tasks with status {}", status);
        return taskRepository.findByStatus(status).stream()
                .map(taskMapper::toResponse)
                .collect(Collectors.toList());
    }

    /**
     * Get all distinct tags for a project
     *
     * @param projectId the project ID
     * @return list of unique tags
     */
    public List<String> findDistinctTags(Long projectId) {
        log.debug("Finding distinct tags for project: {}", projectId);
        return taskRepository.findDistinctTagsByProjectId(projectId);
    }

    /**
     * Count tasks by project and status
     *
     * @param projectId the project ID
     * @param status the task status
     * @return count of tasks
     */
    public Long countByProjectIdAndStatus(Long projectId, TaskStatus status) {
        log.debug("Counting tasks for project {} with status {}", projectId, status);
        return taskRepository.countByProjectIdAndStatus(projectId, status);
    }

    /**
     * Count total tasks for a project
     *
     * @param projectId the project ID
     * @return count of tasks
     */
    public Long countByProjectId(Long projectId) {
        log.debug("Counting tasks for project: {}", projectId);
        return taskRepository.countByProjectId(projectId);
    }

    /**
     * Create a new task
     *
     * @param request the task request
     * @return created task response
     */
    @Transactional
    public TaskResponse create(TaskRequest request) {
        log.debug("Creating task: {}", request);

        // Verify project exists
        Project project = projectRepository.findById(request.getProjectId())
                .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));

        Task task = taskMapper.toEntity(request);
        task.setProject(project);

        Task savedTask = taskRepository.save(task);
        log.info("Task created with id: {}", savedTask.getId());

        return taskMapper.toResponse(savedTask);
    }

    /**
     * Update an existing task
     *
     * @param id the task ID
     * @param request the task request
     * @return updated task response
     */
    @Transactional
    public TaskResponse update(Long id, TaskRequest request) {
        log.debug("Updating task {}: {}", id, request);

        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Task", "id", id));

        // If projectId is changing, verify new project exists
        if (!task.getProject().getId().equals(request.getProjectId())) {
            Project newProject = projectRepository.findById(request.getProjectId())
                    .orElseThrow(() -> new ResourceNotFoundException("Project", "id", request.getProjectId()));
            task.setProject(newProject);
        }

        taskMapper.updateEntityFromRequest(request, task);

        Task updatedTask = taskRepository.save(task);
        log.info("Task updated: {}", id);

        return taskMapper.toResponse(updatedTask);
    }

    /**
     * Delete a task
     *
     * @param id the task ID
     */
    @Transactional
    public void delete(Long id) {
        log.debug("Deleting task: {}", id);

        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Task", "id", id));

        taskRepository.delete(task);
        log.info("Task deleted: {}", id);
    }
}
