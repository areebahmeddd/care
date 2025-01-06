from faker import Faker
from model_bakery import baker
from rest_framework.test import APITestCase

from care.emr.models.organization import OrganizationUser


class CareAPITestBase(APITestCase):
    fake = Faker()

    def create_user(self, **kwargs):
        from care.users.models import User

        return baker.make(User, **kwargs)

    def create_facility(self):
        pass

    def create_organization(self, **kwargs):
        from care.emr.models import Organization

        return baker.make(Organization, **kwargs)

    def create_role(self, **kwargs):
        from care.security.models import RoleModel

        if RoleModel.objects.filter(**kwargs).exists():
            return RoleModel.objects.get(**kwargs)
        return baker.make(RoleModel, **kwargs)

    def create_role_with_permissions(self, permissions):
        from care.security.models import PermissionModel, RoleModel, RolePermission

        role = baker.make(RoleModel)

        for permission in permissions:
            RolePermission.objects.create(
                role=role, permission=baker.make(PermissionModel, slug=permission)
            )
        return role

    def attach_role_organization_user(self, organization, user, role):
        OrganizationUser.objects.create(organization=organization, user=user, role=role)

    def attach_role_facility_organization_user(self):
        pass
