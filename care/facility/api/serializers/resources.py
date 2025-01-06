from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from care.facility.api.serializers import TIMESTAMP_FIELDS
from care.facility.api.serializers.facility import FacilityBasicInfoSerializer
from care.facility.api.serializers.patient import PatientListSerializer
from care.facility.models import (
    RESOURCE_CATEGORY_CHOICES,
    RESOURCE_STATUS_CHOICES,
    Facility,
    PatientRegistration,
    ResourceRequest,
    ResourceRequestComment,
    User,
)
from care.users.api.serializers.user import UserBaseMinimumSerializer
from care.utils.queryset.patient import get_patient_queryset
from care.utils.serializers.fields import ChoiceField, ExternalIdSerializerField


def inverse_choices(choices):
    output = {}
    for choice in choices:
        output[choice[1]] = choice[0]
    return output


REVERSE_REQUEST_STATUS_CHOICES = inverse_choices(RESOURCE_STATUS_CHOICES)


def has_facility_permission(user, facility):
    if not facility:
        return False
    return (
        user.is_superuser
        or (facility and user in facility.users.all())
        or (
            user.user_type >= User.TYPE_VALUE_MAP["DistrictLabAdmin"]
            and (facility and user.district == facility.district)
        )
        or (
            user.user_type >= User.TYPE_VALUE_MAP["StateLabAdmin"]
            and (facility and user.state == facility.state)
        )
    )


class ResourceRequestSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    status = ChoiceField(choices=RESOURCE_STATUS_CHOICES)

    origin_facility_object = FacilityBasicInfoSerializer(
        source="origin_facility", read_only=True, required=False
    )
    approving_facility_object = FacilityBasicInfoSerializer(
        source="approving_facility", read_only=True, required=False
    )
    assigned_facility_object = FacilityBasicInfoSerializer(
        source="assigned_facility", read_only=True, required=False
    )

    category = ChoiceField(choices=RESOURCE_CATEGORY_CHOICES)

    origin_facility = ExternalIdSerializerField(
        queryset=Facility.objects.all(), required=True
    )

    approving_facility = ExternalIdSerializerField(
        queryset=Facility.objects.all(), required=False
    )

    assigned_facility = ExternalIdSerializerField(
        queryset=Facility.objects.all(), required=True
    )

    related_patient = ExternalIdSerializerField(
        queryset=PatientRegistration.objects.all(), required=False, write_only=True
    )

    related_patient_object = PatientListSerializer(
        source="related_patient", read_only=True
    )

    assigned_to_object = UserBaseMinimumSerializer(source="assigned_to", read_only=True)
    created_by_object = UserBaseMinimumSerializer(source="created_by", read_only=True)
    last_edited_by_object = UserBaseMinimumSerializer(
        source="last_edited_by", read_only=True
    )

    def __init__(self, instance=None, **kwargs):
        if instance:
            kwargs["partial"] = True
        super().__init__(instance=instance, **kwargs)

    def update(self, instance, validated_data):
        # ruff: noqa: N806 better to refactor this
        LIMITED_RECIEVING_STATUS_ = [
            "ON HOLD",
            "APPROVED",
            "REJECTED",
            "TRANSPORTATION TO BE ARRANGED",
            "TRANSFER IN PROGRESS",
            "COMPLETED",
        ]
        LIMITED_RECIEVING_STATUS = [
            REVERSE_REQUEST_STATUS_CHOICES[x] for x in LIMITED_RECIEVING_STATUS_
        ]
        LIMITED_REQUEST_STATUS_ = [
            "ON HOLD",
            "APPROVED",
            "REJECTED",
            "TRANSPORTATION TO BE ARRANGED",
            "TRANSFER IN PROGRESS",
            "COMPLETED",
        ]
        LIMITED_REQUEST_STATUS = [
            REVERSE_REQUEST_STATUS_CHOICES[x] for x in LIMITED_REQUEST_STATUS_
        ]

        user = self.context["request"].user

        if "status" in validated_data:
            validated = False
            if validated_data["status"] in LIMITED_RECIEVING_STATUS:
                validated = True
                if (
                    instance.assigned_facility
                    and not user.user_type < User.TYPE_VALUE_MAP["Volunteer"]
                    and not has_facility_permission(user, instance.assigned_facility)
                ):
                    raise ValidationError({"status": ["Permission Denied"]})
            if (
                not validated
                and instance.approving_facility
                and validated_data["status"] in LIMITED_REQUEST_STATUS
                and not User.TYPE_VALUE_MAP[user.user_type]
                < User.TYPE_VALUE_MAP["Volunteer"]
                and not has_facility_permission(user, instance.approving_facility)
            ):
                raise ValidationError({"status": ["Permission Denied"]})

        # Dont allow editing origin or patient
        validated_data.pop("origin_facility", None)
        validated_data.pop("related_patient", None)

        instance.last_edited_by = self.context["request"].user

        return super().update(instance, validated_data)

    def create(self, validated_data):
        # Do Validity checks for each of these data
        if "status" in validated_data:
            validated_data.pop("status")

        user = self.context["request"].user

        if "related_patient" in validated_data:
            allowed_patients = get_patient_queryset(user)
            if not allowed_patients.filter(
                external_id=validated_data["related_patient"].external_id
            ).exists():
                raise ValidationError({"related_patient": ["Permission Denied"]})
        validated_data["created_by"] = user
        validated_data["last_edited_by"] = user

        return super().create(validated_data)

    class Meta:
        model = ResourceRequest
        exclude = ("deleted", "external_id")
        read_only_fields = TIMESTAMP_FIELDS


class ResourceRequestCommentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    created_by_object = UserBaseMinimumSerializer(source="created_by", read_only=True)

    def validate_empty_values(self, data):
        if not data.get("comment", "").strip():
            raise serializers.ValidationError({"comment": ["Comment cannot be empty"]})
        return super().validate_empty_values(data)

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user

        return super().create(validated_data)

    class Meta:
        model = ResourceRequestComment
        exclude = ("deleted", "request", "external_id")
        read_only_fields = (*TIMESTAMP_FIELDS, "created_by")
