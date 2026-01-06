package dev.federicocalo.managementeconomy.entity;

import dev.federicocalo.managementeconomy.enums.TaskStatus;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * Entity representing a task within a project.
 * Tasks help organize and track work items for each project.
 */
@Entity
@Table(name = "tasks")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Task {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * The project this task belongs to
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    /**
     * Task title/name
     */
    @Column(nullable = false)
    private String title;

    /**
     * Tag/category for task organization (e.g., "Backend", "Frontend", "Bug", "Feature")
     */
    @Column(length = 100)
    private String tag;

    /**
     * Detailed description of the task
     */
    @Column(columnDefinition = "TEXT")
    private String description;

    /**
     * Current status of the task
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    @Builder.Default
    private TaskStatus status = TaskStatus.TODO;

    /**
     * Timestamp when the task was created
     */
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    /**
     * Timestamp when the task was last updated
     */
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
