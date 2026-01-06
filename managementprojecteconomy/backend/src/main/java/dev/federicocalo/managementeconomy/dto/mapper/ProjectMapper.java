package dev.federicocalo.managementeconomy.dto.mapper;

import dev.federicocalo.managementeconomy.dto.request.ProjectCreateRequest;
import dev.federicocalo.managementeconomy.dto.request.ProjectUpdateRequest;
import dev.federicocalo.managementeconomy.dto.response.ProjectResponse;
import dev.federicocalo.managementeconomy.entity.Project;
import org.mapstruct.*;

import java.util.List;

/**
 * Mapper MapStruct per conversioni Project DTO <-> Entity
 */
@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface ProjectMapper {

    /**
     * Converte CreateRequest in Entity
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    @Mapping(target = "status", constant = "ACTIVE")
    Project toEntity(ProjectCreateRequest request);

    /**
     * Converte Entity in Response
     */
    ProjectResponse toResponse(Project project);

    /**
     * Converte lista di Entity in lista di Response
     */
    List<ProjectResponse> toResponseList(List<Project> projects);

    /**
     * Aggiorna Entity esistente da UpdateRequest
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "code", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updateEntityFromRequest(ProjectUpdateRequest request, @MappingTarget Project project);
}
