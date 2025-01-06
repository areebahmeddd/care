from pydantic import UUID4
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from care.emr.api.viewsets.base import EMRBaseViewSet, EMRRetrieveMixin
from care.emr.api.viewsets.scheduling import (
    AppointmentBookingSpec,
    SlotsForDayRequestSpec,
    SlotViewSet,
)
from care.emr.models.patient import Patient
from care.emr.models.scheduling import TokenBooking, TokenSlot
from care.emr.resources.scheduling.slot.spec import (
    TokenBookingReadSpec,
    TokenSlotBaseSpec,
)
from config.patient_otp_authentication import (
    JWTTokenPatientAuthentication,
    OTPAuthenticatedPermission,
)


class SlotsForDayRequestSpec(SlotsForDayRequestSpec):
    facility: UUID4


class OTPSlotViewSet(EMRRetrieveMixin, EMRBaseViewSet):
    authentication_classes = [JWTTokenPatientAuthentication]
    permission_classes = [OTPAuthenticatedPermission]
    database_model = TokenSlot
    pydantic_read_model = TokenSlotBaseSpec

    @action(detail=False, methods=["POST"])
    def get_slots_for_day(self, request, *args, **kwargs):
        request_data = SlotsForDayRequestSpec(**request.data)
        return SlotViewSet.get_slots_for_day_handler(
            request_data.facility, request.data
        )

    @action(detail=True, methods=["POST"])
    def create_appointment(self, request, *args, **kwargs):
        request_data = AppointmentBookingSpec(**request.data)
        if not Patient.objects.filter(
            external_id=request_data.patient, phone_number=request.user.phone_number
        ).exists():
            raise ValidationError("Patient not allowed ")
        return SlotViewSet.create_appointment_handler(
            self.get_object(), request.data, None
        )

    @action(detail=False, methods=["GET"])
    def get_appointments(self, request, *args, **kwargs):
        appointments = TokenBooking.objects.filter(
            patient__phone_number=request.user.phone_number
        )
        return Response(
            {
                "results": [
                    TokenBookingReadSpec.serialize(obj).model_dump(exclude=["meta"])
                    for obj in appointments
                ]
            }
        )
