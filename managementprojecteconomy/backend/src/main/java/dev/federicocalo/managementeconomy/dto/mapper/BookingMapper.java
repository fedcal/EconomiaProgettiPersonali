package dev.federicocalo.managementeconomy.dto.mapper;

import dev.federicocalo.managementeconomy.dto.request.BookingCreateRequest;
import dev.federicocalo.managementeconomy.dto.request.BookingUpdateRequest;
import dev.federicocalo.managementeconomy.dto.response.BookingResponse;
import dev.federicocalo.managementeconomy.entity.Booking;
import org.mapstruct.*;

import java.util.List;

/**
 * Mapper MapStruct per conversioni Booking DTO <-> Entity
 */
@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface BookingMapper {

    /**
     * Converte CreateRequest in Entity
     * Nota: project deve essere settato dal service
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "nights", ignore = true)
    @Mapping(target = "pricePerNight", ignore = true)
    @Mapping(target = "commissionRate", ignore = true)
    @Mapping(target = "commissionAmount", ignore = true)
    @Mapping(target = "netRevenue", ignore = true)
    @Mapping(target = "bookingStatus", constant = "CONFIRMED")
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    Booking toEntity(BookingCreateRequest request);

    /**
     * Converte Entity in Response
     */
    @Mapping(source = "project.id", target = "projectId")
    @Mapping(source = "project.name", target = "projectName")
    BookingResponse toResponse(Booking booking);

    /**
     * Converte lista di Entity in lista di Response
     */
    List<BookingResponse> toResponseList(List<Booking> bookings);

    /**
     * Aggiorna Entity esistente da UpdateRequest
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "project", ignore = true)
    @Mapping(target = "nights", ignore = true)
    @Mapping(target = "pricePerNight", ignore = true)
    @Mapping(target = "commissionRate", ignore = true)
    @Mapping(target = "commissionAmount", ignore = true)
    @Mapping(target = "netRevenue", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updateEntityFromRequest(BookingUpdateRequest request, @MappingTarget Booking booking);
}
