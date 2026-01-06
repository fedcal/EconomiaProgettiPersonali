package dev.federicocalo.managementeconomy.mapper;

import dev.federicocalo.managementeconomy.dto.request.OneTimeCostRequest;
import dev.federicocalo.managementeconomy.dto.request.RecurringCostRequest;
import dev.federicocalo.managementeconomy.dto.response.OneTimeCostResponse;
import dev.federicocalo.managementeconomy.dto.response.RecurringCostResponse;
import dev.federicocalo.managementeconomy.entity.OneTimeCost;
import dev.federicocalo.managementeconomy.entity.RecurringCost;
import org.mapstruct.*;

/**
 * MapStruct mapper for OneTimeCost and RecurringCost entities
 */
@Mapper(componentModel = "spring", nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
public interface CostMapper {

    // OneTimeCost mappings
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    OneTimeCost toEntity(OneTimeCostRequest request);

    @Mapping(source = "project.id", target = "projectId")
    @Mapping(source = "project.name", target = "projectName")
    OneTimeCostResponse toResponse(OneTimeCost entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    void updateEntityFromRequest(OneTimeCostRequest request, @MappingTarget OneTimeCost entity);

    // RecurringCost mappings
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    RecurringCost toEntity(RecurringCostRequest request);

    @Mapping(source = "project.id", target = "projectId")
    @Mapping(source = "project.name", target = "projectName")
    RecurringCostResponse toResponse(RecurringCost entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    void updateEntityFromRequest(RecurringCostRequest request, @MappingTarget RecurringCost entity);
}
