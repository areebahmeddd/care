from django.db import transaction
from django_filters import FilterSet, UUIDFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404

from care.emr.api.viewsets.base import EMRModelViewSet
from care.emr.models.organization import FacilityOrganizationUser
from care.emr.models.scheduling.schedule import Schedule
from care.emr.resources.scheduling.schedule.spec import (
    ScheduleReadSpec,
    ScheduleUpdateSpec,
    ScheduleWriteSpec,
)
from care.facility.models import Facility
from care.security.authorization import AuthorizationController
from care.users.models import User


class ScheduleFilters(FilterSet):
    user = UUIDFilter(field_name="resource__user__external_id")


class ScheduleViewSet(EMRModelViewSet):
    database_model = Schedule
    pydantic_model = ScheduleWriteSpec
    pydantic_update_model = ScheduleUpdateSpec
    pydantic_read_model = ScheduleReadSpec
    filterset_class = ScheduleFilters
    filter_backends = [DjangoFilterBackend]
    CREATE_QUESTIONNAIRE_RESPONSE = False

    def get_facility_obj(self):
        return get_object_or_404(
            Facility, external_id=self.kwargs["facility_external_id"]
        )

    def perform_create(self, instance):
        with transaction.atomic():
            super().perform_create(instance)
            for availability in instance.availabilities:
                availability_obj = availability.de_serialize()
                availability_obj.schedule = instance
                availability_obj.save()

    def authorize_delete(self, instance):
        self.authorize_update({}, instance)

    def validate_data(self, instance, model_obj=None):
        # Validate user is part of the facility
        facility = self.get_facility_obj()
        schedule_user = get_object_or_404(User, external_id=instance.user)
        if not FacilityOrganizationUser.objects.filter(
            user=schedule_user, organization__facility=facility
        ).exists():
            raise ValidationError("Schedule User is not part of the facility")

    def authorize_create(self, instance):
        facility = self.get_facility_obj()
        schedule_user = get_object_or_404(User, external_id=instance.user)
        if not AuthorizationController.call(
            "can_write_user_schedule", self.request.user, facility, schedule_user
        ):
            raise PermissionDenied("You do not have permission to view user schedule")

    def authorize_update(self, request_obj, model_instance):
        if not AuthorizationController.call(
            "can_write_user_schedule",
            self.request.user,
            model_instance.resource.facility,
            model_instance.resource.user,
        ):
            raise PermissionDenied("You do not have permission to view user schedule")

    def clean_create_data(self, request_data):
        request_data["facility"] = self.kwargs["facility_external_id"]
        return request_data

    def get_queryset(self):
        facility = self.get_facility_obj()
        if not AuthorizationController.call(
            "can_list_user_schedule", self.request.user, facility
        ):
            raise PermissionDenied("You do not have permission to view user schedule")
        return (
            super()
            .get_queryset()
            .filter(resource__facility=facility)
            .select_related("resource", "created_by", "updated_by")
            .order_by("-modified_date")
        )
