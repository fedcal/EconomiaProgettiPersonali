package dev.federicocalo.managementeconomy.repository;

import dev.federicocalo.managementeconomy.entity.Task;
import dev.federicocalo.managementeconomy.enums.TaskStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for Task entity operations.
 */
@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {

    /**
     * Find all tasks for a specific project
     *
     * @param projectId the project ID
     * @return list of tasks
     */
    @Query("SELECT t FROM Task t WHERE t.project.id = :projectId ORDER BY t.createdAt DESC")
    List<Task> findByProjectId(@Param("projectId") Long projectId);

    /**
     * Find tasks by project and status
     *
     * @param projectId the project ID
     * @param status the task status
     * @return list of tasks
     */
    @Query("SELECT t FROM Task t WHERE t.project.id = :projectId AND t.status = :status ORDER BY t.createdAt DESC")
    List<Task> findByProjectIdAndStatus(@Param("projectId") Long projectId, @Param("status") TaskStatus status);

    /**
     * Find tasks by tag
     *
     * @param projectId the project ID
     * @param tag the tag
     * @return list of tasks
     */
    @Query("SELECT t FROM Task t WHERE t.project.id = :projectId AND t.tag = :tag ORDER BY t.createdAt DESC")
    List<Task> findByProjectIdAndTag(@Param("projectId") Long projectId, @Param("tag") String tag);

    /**
     * Find all tasks by status across all projects
     *
     * @param status the task status
     * @return list of tasks
     */
    List<Task> findByStatus(TaskStatus status);

    /**
     * Count tasks by project and status
     *
     * @param projectId the project ID
     * @param status the task status
     * @return count of tasks
     */
    @Query("SELECT COUNT(t) FROM Task t WHERE t.project.id = :projectId AND t.status = :status")
    Long countByProjectIdAndStatus(@Param("projectId") Long projectId, @Param("status") TaskStatus status);

    /**
     * Count total tasks for a project
     *
     * @param projectId the project ID
     * @return count of tasks
     */
    @Query("SELECT COUNT(t) FROM Task t WHERE t.project.id = :projectId")
    Long countByProjectId(@Param("projectId") Long projectId);

    /**
     * Get all distinct tags for a project
     *
     * @param projectId the project ID
     * @return list of unique tags
     */
    @Query("SELECT DISTINCT t.tag FROM Task t WHERE t.project.id = :projectId AND t.tag IS NOT NULL ORDER BY t.tag")
    List<String> findDistinctTagsByProjectId(@Param("projectId") Long projectId);
}
