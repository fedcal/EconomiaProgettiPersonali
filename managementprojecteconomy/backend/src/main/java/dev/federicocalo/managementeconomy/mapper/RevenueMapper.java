package dev.federicocalo.managementeconomy.mapper;

import dev.federicocalo.managementeconomy.dto.request.RevenueStreamRequest;
import dev.federicocalo.managementeconomy.dto.response.RevenueStreamResponse;
import dev.federicocalo.managementeconomy.entity.RevenueStream;
import org.mapstruct.*;

/**
 * MapStruct mapper for RevenueStream entity
 */
@Mapper(componentModel = "spring", nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
public interface RevenueMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    RevenueStream toEntity(RevenueStreamRequest request);

    @Mapping(source = "project.id", target = "projectId")
    @Mapping(source = "project.name", target = "projectName")
    RevenueStreamResponse toResponse(RevenueStream entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    void updateEntityFromRequest(RevenueStreamRequest request, @MappingTarget RevenueStream entity);
}
