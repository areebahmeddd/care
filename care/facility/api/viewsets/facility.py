from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from djqscsv import render_to_csv_response
from drf_spectacular.utils import extend_schema, extend_schema_view
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import filters as drf_filters
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from care.emr.models import Organization
from care.emr.models.organization import FacilityOrganizationUser, OrganizationUser
from care.emr.resources.user.spec import UserSpec
from care.facility.api.serializers.facility import (
    FacilityBasicInfoSerializer,
    FacilityImageUploadSerializer,
    FacilitySerializer,
    FacilitySpokeSerializer,
)
from care.facility.models import (
    Facility,
    FacilityCapacity,
    HospitalDoctors,
)
from care.facility.models.facility import FacilityHubSpoke
from care.users.models import User
from care.utils.file_uploads.cover_image import delete_cover_image
from care.utils.queryset.facility import get_facility_queryset


class GeoOrganizationFilter(filters.UUIDFilter):
    def filter(self, qs, value):
        if value:
            organization = get_object_or_404(Organization, external_id=value)
            return qs.filter(geo_organization_cache__overlap=[organization.id])
        return qs


class FacilityFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    facility_type = filters.NumberFilter(field_name="facility_type")
    organization = GeoOrganizationFilter()


class FacilityViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for facility CRUD operations."""

    queryset = Facility.objects.all().select_related()
    filter_backends = (
        filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
    )
    filterset_class = FacilityFilter
    lookup_field = "external_id"

    search_fields = ["name"]

    FACILITY_CAPACITY_CSV_KEY = "capacity"
    FACILITY_DOCTORS_CSV_KEY = "doctors"
    FACILITY_TRIAGE_CSV_KEY = "triage"

    def get_queryset(self):
        # TODO Add Permission checks
        organization_ids = list(
            OrganizationUser.objects.filter(user=self.request.user).values_list(
                "organization_id", flat=True
            )
        )
        return (
            super()
            .get_queryset()
            .filter(
                Q(
                    id__in=FacilityOrganizationUser.objects.filter(
                        user=self.request.user
                    ).values_list("organization__facility_id")
                )
                | Q(geo_organization_cache__overlap=organization_ids)
            )
        )

    def get_serializer_class(self):
        if self.request.query_params.get("all") == "true":
            return FacilityBasicInfoSerializer
        if self.action == "cover_image":
            # Check DRYpermissions before updating
            return FacilityImageUploadSerializer
        return FacilitySerializer

    def list(self, request, *args, **kwargs):
        if settings.CSV_REQUEST_PARAMETER in request.GET:
            mapping = Facility.CSV_MAPPING.copy()
            pretty_mapping = Facility.CSV_MAKE_PRETTY.copy()
            if self.FACILITY_CAPACITY_CSV_KEY in request.GET:
                mapping.update(FacilityCapacity.CSV_RELATED_MAPPING.copy())
                pretty_mapping.update(FacilityCapacity.CSV_MAKE_PRETTY.copy())
            elif self.FACILITY_DOCTORS_CSV_KEY in request.GET:
                mapping.update(HospitalDoctors.CSV_RELATED_MAPPING.copy())
                pretty_mapping.update(HospitalDoctors.CSV_MAKE_PRETTY.copy())
            queryset = self.filter_queryset(self.get_queryset()).values(*mapping.keys())
            return render_to_csv_response(
                queryset, field_header_map=mapping, field_serializer_map=pretty_mapping
            )

        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["facility"])
    @method_decorator(parser_classes([MultiPartParser]))
    @action(methods=["POST"], detail=True)
    def cover_image(self, request, external_id):
        facility = self.get_object()
        serializer = FacilityImageUploadSerializer(facility, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(tags=["facility"])
    @cover_image.mapping.delete
    def cover_image_delete(self, *args, **kwargs):
        facility = self.get_object()
        delete_cover_image(facility.cover_image_url, "cover_images")
        facility.cover_image_url = None
        facility.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["GET"])
    def users(self, request, *args, **kwargs):
        facility = self.get_object()
        facility_orgs = FacilityOrganizationUser.objects.filter(
            organization__facility=facility
        )
        users = User.objects.filter(id__in=facility_orgs.values("user_id"))
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(users, request)
        data = [UserSpec.serialize(obj).to_json() for obj in page]
        return paginator.get_paginated_response(data)


@extend_schema_view(
    list=extend_schema(tags=["facility"]),
    retrieve=extend_schema(tags=["facility"]),
)
class AllFacilityViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = ()
    authentication_classes = ()
    queryset = Facility.objects.filter(is_public=True).select_related()
    serializer_class = FacilityBasicInfoSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = FacilityFilter
    lookup_field = "external_id"
    search_fields = ["name"]


class FacilitySpokesViewSet(viewsets.ModelViewSet):
    queryset = FacilityHubSpoke.objects.all().select_related("spoke", "hub")
    serializer_class = FacilitySpokeSerializer
    permission_classes = (IsAuthenticated, DRYPermissions)
    lookup_field = "external_id"

    def get_queryset(self):
        return self.queryset.filter(hub=self.get_facility())

    def get_facility(self):
        facilities = get_facility_queryset(self.request.user)
        return get_object_or_404(
            facilities.filter(external_id=self.kwargs["facility_external_id"])
        )

    def get_serializer_context(self):
        facility = self.get_facility()
        context = super().get_serializer_context()
        context["facility"] = facility
        return context


class FacilityHubsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = FacilityHubSpoke.objects.all().select_related("spoke", "hub")
    serializer_class = FacilitySpokeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "external_id"

    def get_queryset(self):
        return self.queryset.filter(spoke=self.get_facility())

    def get_facility(self):
        facilities = get_facility_queryset(self.request.user)
        return get_object_or_404(
            facilities.filter(external_id=self.kwargs["facility_external_id"])
        )
