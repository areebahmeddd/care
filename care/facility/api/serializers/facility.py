from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from care.emr.models import Organization
from care.emr.resources.organization.spec import OrganizationReadSpec
from care.facility.models import FACILITY_TYPES, Facility, FacilityLocalGovtBody
from care.facility.models.facility import FEATURE_CHOICES, FacilityHubSpoke
from care.users.api.serializers.lsg import (
    DistrictSerializer,
    LocalBodySerializer,
)
from care.utils.file_uploads.cover_image import upload_cover_image
from care.utils.models.validators import (
    MiddlewareDomainAddressValidator,
    cover_image_validator,
    custom_image_extension_validator,
)
from care.utils.serializers.fields import ChoiceField, ExternalIdSerializerField

User = get_user_model()


class FacilityLocalGovtBodySerializer(serializers.ModelSerializer):
    local_body = LocalBodySerializer()
    district = DistrictSerializer()

    class Meta:
        model = FacilityLocalGovtBody
        fields = "__all__"


class FacilityBareMinimumSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)

    class Meta:
        model = Facility
        fields = (
            "id",
            "name",
        )


class FacilityBasicInfoSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    facility_type = serializers.SerializerMethodField()
    read_cover_image_url = serializers.CharField(read_only=True)
    features = serializers.ListField(
        child=serializers.ChoiceField(choices=FEATURE_CHOICES),
        required=False,
    )
    geo_organization_obj = serializers.SerializerMethodField(read_only=True)

    def get_facility_type(self, facility):
        return {
            "id": facility.facility_type,
            "name": facility.get_facility_type_display(),
        }

    def get_geo_organization_obj(self, facility):
        if facility.geo_organization:
            return OrganizationReadSpec.serialize(facility.geo_organization).to_json()
        return None

    class Meta:
        model = Facility
        fields = (
            "id",
            "name",
            "description",
            "facility_type",
            "read_cover_image_url",
            "features",
            "geo_organization_obj",
        )


class FacilitySerializer(FacilityBasicInfoSerializer):
    """Serializer for facility.models.Facility."""

    facility_type = ChoiceField(choices=FACILITY_TYPES)
    read_cover_image_url = serializers.URLField(read_only=True)
    features = serializers.ListField(
        child=serializers.ChoiceField(choices=FEATURE_CHOICES),
        required=False,
    )
    geo_organization = ExternalIdSerializerField(
        Organization.objects.filter(org_type="govt"), write_only=True
    )

    geo_organization_obj = serializers.SerializerMethodField(read_only=True)

    facility_flags = serializers.SerializerMethodField()

    def get_facility_flags(self, facility):
        return facility.get_facility_flags()

    def get_geo_organization_obj(self, facility):
        if facility.geo_organization:
            return OrganizationReadSpec.serialize(facility.geo_organization).to_json()
        return None

    class Meta:
        model = Facility
        fields = [
            "id",
            "name",
            "description",
            "facility_type",
            "address",
            "longitude",
            "latitude",
            "features",
            "pincode",
            "phone_number",
            "modified_date",
            "created_date",
            "middleware_address",
            "read_cover_image_url",
            "facility_flags",
            "geo_organization",
            "geo_organization_obj",
        ]
        read_only_fields = ("modified_date", "created_date")

    def validate_middleware_address(self, value):
        if not value:
            msg = "Middleware Address is required"
            raise serializers.ValidationError(msg)
        value = value.strip()
        if not value:
            return value

        # Check if the address is valid
        MiddlewareDomainAddressValidator()(value)
        return value

    def validate_features(self, value):
        if len(value) != len(set(value)):
            msg = "Features should not contain duplicate values."
            raise serializers.ValidationError(msg)
        return value

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class FacilitySpokeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="external_id", read_only=True)
    spoke = ExternalIdSerializerField(
        queryset=Facility.objects.all(), required=True, write_only=True
    )
    hub_object = FacilityBasicInfoSerializer(read_only=True, source="hub")
    spoke_object = FacilityBasicInfoSerializer(read_only=True, source="spoke")

    class Meta:
        model = FacilityHubSpoke
        fields = (
            "id",
            "spoke",
            "hub_object",
            "spoke_object",
            "relationship",
            "created_date",
            "modified_date",
        )
        read_only_fields = (
            "id",
            "spoke_object",
            "hub_object",
            "created_date",
            "modified_date",
        )

    def validate(self, data):
        data["hub"] = self.context["facility"]
        return data

    def validate_spoke(self, spoke: Facility):
        hub: Facility = self.context["facility"]

        if hub == spoke:
            msg = "Cannot set a facility as it's own spoke"
            raise serializers.ValidationError(msg)

        if FacilityHubSpoke.objects.filter(
            Q(hub=hub, spoke=spoke) | Q(hub=spoke, spoke=hub)
        ).first():
            msg = "Facility is already a spoke/hub"
            raise serializers.ValidationError(msg)

        return spoke


class FacilityImageUploadSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(
        required=True,
        write_only=True,
        validators=[custom_image_extension_validator, cover_image_validator],
    )
    read_cover_image_url = serializers.URLField(read_only=True)

    class Meta:
        model = Facility
        # Check DRYpermissions before updating
        fields = ("cover_image", "read_cover_image_url")

    def save(self, **kwargs):
        facility: Facility = self.instance
        image = self.validated_data["cover_image"]
        facility.cover_image_url = upload_cover_image(
            image,
            str(facility.external_id),
            "cover_images",
            facility.cover_image_url,
        )
        facility.save(update_fields=["cover_image_url"])
        return facility
