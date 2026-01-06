package dev.federicocalo.managementeconomy.enums;

/**
 * Enum representing the status of a task.
 */
public enum TaskStatus {
    /**
     * Task is planned but not yet started
     */
    TODO,

    /**
     * Task is currently being worked on
     */
    IN_PROGRESS,

    /**
     * Task has been completed
     */
    COMPLETED,

    /**
     * Task is blocked by dependencies or external factors
     */
    BLOCKED,

    /**
     * Task has been cancelled and will not be completed
     */
    CANCELLED
}
