package dev.federicocalo.managementeconomy.dto;

import dev.federicocalo.managementeconomy.enums.TaskStatus;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * DTO for creating or updating a task.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TaskRequest {

    /**
     * The project ID this task belongs to
     */
    @NotNull(message = "Project ID is required")
    private Long projectId;

    /**
     * Task title
     */
    @NotBlank(message = "Title is required")
    @Size(max = 255, message = "Title must not exceed 255 characters")
    private String title;

    /**
     * Task tag/category
     */
    @Size(max = 100, message = "Tag must not exceed 100 characters")
    private String tag;

    /**
     * Task description
     */
    private String description;

    /**
     * Task status
     */
    @NotNull(message = "Status is required")
    private TaskStatus status;
}
