import datetime
from datetime import time, timedelta

from dateutil.parser import parse
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from pydantic import UUID4, BaseModel, model_validator
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from care.emr.api.viewsets.base import EMRBaseViewSet, EMRRetrieveMixin
from care.emr.models import AvailabilityException, Schedule, TokenBooking
from care.emr.models.patient import Patient
from care.emr.models.scheduling.booking import TokenSlot
from care.emr.models.scheduling.schedule import Availability, SchedulableUserResource
from care.emr.resources.scheduling.schedule.spec import SlotTypeOptions
from care.emr.resources.scheduling.slot.spec import (
    TokenBookingReadSpec,
    TokenSlotBaseSpec,
)
from care.security.authorization import AuthorizationController
from care.users.models import User
from care.utils.lock import Lock


class SlotsForDayRequestSpec(BaseModel):
    user: UUID4
    day: datetime.date


class AppointmentBookingSpec(BaseModel):
    patient: UUID4
    reason_for_visit: str


class AvailabilityStatsRequestSpec(BaseModel):
    from_date: datetime.date
    to_date: datetime.date
    user: UUID4

    @model_validator(mode="after")
    def validate_period(self):
        max_period = 32
        if self.from_date > self.to_date:
            raise ValidationError("From Date cannot be greater than To Date")
        if self.from_date - self.to_date > datetime.timedelta(days=max_period):
            raise ValidationError("Period cannot be be greater than max days")


def convert_availability_to_slots(availabilities):
    slots = {}
    for availability in availabilities:
        start_time = parse(availability["availability"]["start_time"])
        end_time = parse(availability["availability"]["end_time"])
        slot_size_in_minutes = availability["slot_size_in_minutes"]
        availability_id = availability["availability_id"]
        current_time = start_time
        i = 0
        while current_time < end_time:
            i += 1
            if i == 30:  # noqa PLR2004
                # Failsafe to prevent infinite loop
                break
            slots[
                f"{current_time.time()}-{(current_time + datetime.timedelta(minutes=slot_size_in_minutes)).time()}"
            ] = {
                "start_time": current_time.time(),
                "end_time": (
                    current_time + datetime.timedelta(minutes=slot_size_in_minutes)
                ).time(),
                "availability_id": availability_id,
            }

            current_time += datetime.timedelta(minutes=slot_size_in_minutes)
    return slots


def lock_create_appointment(token_slot, patient, created_by, reason_for_visit):
    with Lock(f"booking:resource:{token_slot.resource.id}"), transaction.atomic():
        if token_slot.allocated >= token_slot.availability.tokens_per_slot:
            raise ValidationError("Slot is already full")
        token_slot.allocated += 1
        token_slot.save()
        return TokenBooking.objects.create(
            token_slot=token_slot,
            patient=patient,
            booked_by=created_by,
            reason_for_visit=reason_for_visit,
            status="booked",
        )


class SlotViewSet(EMRRetrieveMixin, EMRBaseViewSet):
    database_model = TokenSlot
    pydantic_read_model = TokenSlotBaseSpec

    @action(detail=False, methods=["POST"])
    def get_slots_for_day(self, request, *args, **kwargs):
        return self.get_slots_for_day_handler(
            self.kwargs["facility_external_id"], request.data
        )

    @classmethod
    def get_slots_for_day_handler(cls, facility_external_id, request_data):
        request_data = SlotsForDayRequestSpec(**request_data)
        user = get_object_or_404(User, external_id=request_data.user)
        schedulable_resource_obj = SchedulableUserResource.objects.filter(
            facility__external_id=facility_external_id,
            user=user,
        ).first()
        if not schedulable_resource_obj:
            raise ValidationError("Resource is not schedulable")
        # Find all relevant schedules
        availabilities = Availability.objects.filter(
            slot_type=SlotTypeOptions.appointment.value,
            schedule__valid_from__lte=request_data.day,
            schedule__valid_to__gte=request_data.day,
            schedule__resource=schedulable_resource_obj,
        )
        # Fetch all availabilities for that day of week
        calculated_dow_availabilities = []
        for schedule_availability in availabilities:
            for day_availability in schedule_availability.availability:
                if day_availability["day_of_week"] == request_data.day.weekday():
                    calculated_dow_availabilities.append(
                        {
                            "availability": day_availability,
                            "slot_size_in_minutes": schedule_availability.slot_size_in_minutes,
                            "availability_id": schedule_availability.id,
                        }
                    )
        # Remove anything that has an availability exception
        # Generate all slots already created for that day
        slots = convert_availability_to_slots(calculated_dow_availabilities)
        # Fetch all existing slots in that day
        created_slots = TokenSlot.objects.filter(
            start_datetime__date=request_data.day,
            end_datetime__date=request_data.day,
            resource=schedulable_resource_obj,
        )
        for slot in created_slots:
            slot_key = f"{slot.start_datetime.time()}-{slot.end_datetime.time()}"
            if (
                slot_key in slots
                and slots[slot_key]["availability_id"] == slot.availability.id
            ):
                slots.pop(slot_key)

        # Create everything else
        for _slot in slots:
            slot = slots[_slot]
            TokenSlot.objects.create(
                resource=schedulable_resource_obj,
                start_datetime=datetime.datetime.combine(
                    request_data.day, slot["start_time"], tzinfo=timezone.now().tzinfo
                ),
                end_datetime=datetime.datetime.combine(
                    request_data.day, slot["end_time"], tzinfo=timezone.now().tzinfo
                ),
                availability_id=slot["availability_id"],
            )
        # Compare and figure out what needs to be created
        return Response(
            {
                "results": [
                    TokenSlotBaseSpec.serialize(slot).model_dump(exclude=["meta"])
                    for slot in TokenSlot.objects.filter(
                        start_datetime__date=request_data.day,
                        end_datetime__date=request_data.day,
                        resource=schedulable_resource_obj,
                    ).select_related("availability")
                ]
            }
        )
        # Find all existing Slot objects for that period
        # Get list of all slots, create if missed
        # Return slots

    @classmethod
    def create_appointment_handler(cls, obj, request_data, user):
        request_data = AppointmentBookingSpec(**request_data)
        patient = Patient.objects.filter(external_id=request_data.patient).first()
        if not patient:
            raise ValidationError({"Patient not found"})
        appointment = lock_create_appointment(
            obj, patient, user, request_data.reason_for_visit
        )
        return Response(
            TokenBookingReadSpec.serialize(appointment).model_dump(exclude=["meta"])
        )

    @action(detail=True, methods=["POST"])
    def create_appointment(self, request, *args, **kwargs):
        slot_obj = self.get_object()
        facility = slot_obj.resource.facility
        if not AuthorizationController.call(
            "can_create_appointment", self.request.user, facility
        ):
            raise PermissionDenied("You do not have permission to create appointments")
        return self.create_appointment_handler(slot_obj, request.data, request.user)

    @action(detail=False, methods=["POST"])
    def availability_stats(self, request, *args, **kwargs):
        """
        Return the stats for available slots compared to the booked slots
        ie Availability percentage.
        """
        request_data = AvailabilityStatsRequestSpec(**request.data)
        # Fetch the entire schedule and calculate total slots available for each day
        user = User.objects.filter(external_id=request_data.user).first()
        if not user:
            raise ValidationError("User does not exist")
        resource = SchedulableUserResource.objects.filter(user=user).first()
        if not resource:
            raise ValidationError("Resource is not schedulable")

        schedules = Schedule.objects.filter(
            valid_from__lte=request_data.to_date,
            valid_to__gte=request_data.from_date,
            resource=resource,
        ).values()

        # Cache availabilities
        availabilities = {}
        for schedule in schedules:
            availabilities[schedule["id"]] = Availability.objects.filter(
                schedule_id=schedule["id"],
                slot_type=SlotTypeOptions.appointment.value,
            ).values()

        availability_exceptions = AvailabilityException.objects.filter(
            valid_from__lte=request_data.to_date,
            valid_to__gte=request_data.from_date,
            resource=resource,
        ).values()

        # Generate a list of all available days as a dict

        days = {}
        response_days = {}
        day = request_data.from_date
        while day < request_data.to_date:
            days[day] = {"total_slots": 0, "booked_slots": 0}
            response_days[str(day)] = {"total_slots": 0, "booked_slots": 0}
            day += timedelta(days=1)

        for day in days:
            # Calculate all matching schedules
            current_schedules = []
            for schedule in schedules:
                if schedule["valid_from"].date() <= day <= schedule["valid_to"].date():
                    current_schedules.append(schedule)
            # Calculate availability exception for that day
            exceptions = []
            for exception in availability_exceptions:
                if exception["valid_from"] <= day <= exception["valid_to"]:
                    exceptions.append(exception)
            # Calculate slots based on these data

            slots_count = calculate_slots(
                day, availabilities, current_schedules, exceptions
            )
            days[day]["total_slots"] = slots_count
            response_days[str(day)]["total_slots"] = slots_count
        # Query slots data for these dates, group by date and sum up count

        booked_slots = (
            TokenSlot.objects.filter(
                start_datetime__lte=request_data.to_date,
                end_datetime__gt=request_data.from_date,
                resource=resource,
            )
            .values("start_datetime__date")
            .annotate(allocated_sum=Sum("allocated"))
            .values("allocated_sum", "start_datetime__date")
        )

        for slot in booked_slots:
            response_days[str(slot["start_datetime__date"])]["booked_slots"] = slot[
                "allocated_sum"
            ]
        # Query all the booked slots for the given days and get the total booked

        return Response(response_days)


def calculate_slots(
    date: datetime.date,
    availabilities: list[Availability],
    schedules,
    exceptions: list[AvailabilityException],
):
    # We don't care about duplicate slots because they won't exist because of our validations
    day_of_week = date.weekday()
    slots = 0
    for schedule in schedules:
        for availability in availabilities[schedule["id"]]:
            for available_slot in availability["availability"]:
                if available_slot["day_of_week"] != day_of_week:
                    continue
                start_time = time.fromisoformat(available_slot["start_time"])
                end_time = time.fromisoformat(available_slot["end_time"])
                while start_time <= end_time:
                    conflicting = False
                    for exception in exceptions:
                        if (
                            exception["start_time"] <= end_time
                            and exception["end_time"] >= start_time
                        ):
                            conflicting = True
                    start_time = (
                        datetime.datetime.combine(date.today(), start_time)
                        + timedelta(minutes=availability["slot_size_in_minutes"])
                    ).time()
                    if conflicting:
                        continue
                    slots += availability["tokens_per_slot"]
    return slots
