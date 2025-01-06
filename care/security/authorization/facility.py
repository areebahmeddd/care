from care.security.authorization.base import (
    AuthorizationController,
    AuthorizationHandler,
)
from care.security.permissions.facility import FacilityPermissions


class FacilityAccess(AuthorizationHandler):
    def can_create_facility(self, user):
        return self.check_permission_in_organization(
            [FacilityPermissions.can_create_facility.name], user
        )

    def can_update_facility_obj(self, user, facility):
        return self.check_permission_in_organization(
            [FacilityPermissions.can_update_facility.name],
            user,
            orgs=facility.geo_organization_cache,
        ) or self.check_permission_in_facility_organization(
            [FacilityPermissions.can_update_facility.name], user, facility=facility
        )


AuthorizationController.register_internal_controller(FacilityAccess)
