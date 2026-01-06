package dev.federicocalo.managementeconomy.mapper;

import dev.federicocalo.managementeconomy.dto.TaskRequest;
import dev.federicocalo.managementeconomy.dto.TaskResponse;
import dev.federicocalo.managementeconomy.entity.Task;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

/**
 * MapStruct mapper for Task entity and DTOs.
 */
@Mapper(componentModel = "spring")
public interface TaskMapper {

    /**
     * Convert Task entity to TaskResponse DTO
     *
     * @param task the task entity
     * @return task response DTO
     */
    @Mapping(source = "project.id", target = "projectId")
    @Mapping(source = "project.name", target = "projectName")
    TaskResponse toResponse(Task task);

    /**
     * Convert TaskRequest DTO to Task entity
     *
     * @param request the task request DTO
     * @return task entity
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    Task toEntity(TaskRequest request);

    /**
     * Update existing Task entity from TaskRequest DTO
     *
     * @param request the task request DTO
     * @param task the existing task entity
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    void updateEntityFromRequest(TaskRequest request, @MappingTarget Task task);
}
