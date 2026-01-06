package dev.federicocalo.managementeconomy.mapper;

import dev.federicocalo.managementeconomy.dto.request.SubscriptionRequest;
import dev.federicocalo.managementeconomy.dto.response.SubscriptionResponse;
import dev.federicocalo.managementeconomy.entity.Subscription;
import org.mapstruct.*;

/**
 * MapStruct mapper for Subscription entity
 */
@Mapper(componentModel = "spring", nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
public interface SubscriptionMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    Subscription toEntity(SubscriptionRequest request);

    @Mapping(source = "project.id", target = "projectId")
    @Mapping(source = "project.name", target = "projectName")
    SubscriptionResponse toResponse(Subscription entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    void updateEntityFromRequest(SubscriptionRequest request, @MappingTarget Subscription entity);
}
