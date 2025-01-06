from django.db.models import Q
from django.utils import timezone
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from care.emr.api.viewsets.base import EMRModelViewSet, EMRQuestionnaireResponseMixin
from care.emr.api.viewsets.encounter_authz_base import EncounterBasedAuthorizationBase
from care.emr.models.medication_request import MedicationRequest
from care.emr.registries.system_questionnaire.system_questionnaire import (
    InternalQuestionnaireRegistry,
)
from care.emr.resources.medication.request.spec import (
    MedicationRequestDiscontinueRequest,
    MedicationRequestReadSpec,
    MedicationRequestSpec,
    MedicationRequestStatus,
)
from care.emr.resources.questionnaire.spec import SubjectType


class MedicationRequestFilter(filters.FilterSet):
    encounter = filters.UUIDFilter(field_name="encounter__external_id")
    status = filters.CharFilter(method="filter_statuses")
    is_prn = filters.BooleanFilter(field_name="dosage_instruction__as_needed_boolean")

    def filter_statuses(self, queryset, name, value):
        """
        Handle multiple values for the same 'status' parameter in an OR-fashion
        (case-insensitive).
        """

        # Get *all* values for 'status' as a list: ["active", "on_hold", ...]
        values = self.request.GET.getlist("status")
        if not values:
            return queryset

        query = Q()
        for v in values:
            query |= Q(status__iexact=v)

        return queryset.filter(query)


class MedicationRequestViewSet(
    EncounterBasedAuthorizationBase, EMRQuestionnaireResponseMixin, EMRModelViewSet
):
    database_model = MedicationRequest
    pydantic_model = MedicationRequestSpec
    pydantic_read_model = MedicationRequestReadSpec
    questionnaire_type = "medication_request"
    questionnaire_title = "Medication Request"
    questionnaire_description = "Medication Request"
    questionnaire_subject_type = SubjectType.patient.value
    filterset_class = MedicationRequestFilter
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        self.authorize_read_encounter()
        return (
            super()
            .get_queryset()
            .filter(patient__external_id=self.kwargs["patient_external_id"])
            .select_related("patient", "encounter", "created_by", "updated_by")
        )

    @extend_schema(
        request=MedicationRequestDiscontinueRequest,
        responses={200: MedicationRequestReadSpec},
        tags=["medication_request"],
    )
    @action(detail=True, methods=["POST"])
    def discontinue(self, request, *args, **kwargs):
        data = MedicationRequestDiscontinueRequest(**request.data)
        request: MedicationRequest = self.get_object()
        self.authorize_update({}, request)
        request.status = MedicationRequestStatus.ended
        request.status_changed = timezone.now()
        request.status_reason = data.status_reason
        request.save()

        return Response(
            self.get_read_pydantic_model().serialize(request).to_json(),
        )


InternalQuestionnaireRegistry.register(MedicationRequestViewSet)
