package dev.federicocalo.managementeconomy.dto;

import dev.federicocalo.managementeconomy.enums.TaskStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * DTO for task response.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TaskResponse {

    /**
     * Task ID
     */
    private Long id;

    /**
     * Project ID
     */
    private Long projectId;

    /**
     * Project name (for convenience)
     */
    private String projectName;

    /**
     * Task title
     */
    private String title;

    /**
     * Task tag/category
     */
    private String tag;

    /**
     * Task description
     */
    private String description;

    /**
     * Task status
     */
    private TaskStatus status;

    /**
     * Creation timestamp
     */
    private LocalDateTime createdAt;

    /**
     * Last update timestamp
     */
    private LocalDateTime updatedAt;
}
