import enum

from care.security.permissions.constants import Permission, PermissionContext
from care.security.roles.role import (
    ADMIN_ROLE,
    DOCTOR_ROLE,
    FACILITY_ADMIN_ROLE,
    GEO_ADMIN,
    NURSE_ROLE,
    STAFF_ROLE,
    VOLUNTEER_ROLE,
)


class UserPermissions(enum.Enum):
    can_create_user = Permission(
        "Can create User in care",
        "",
        PermissionContext.FACILITY,
        [ADMIN_ROLE, FACILITY_ADMIN_ROLE, GEO_ADMIN],
    )
    can_list_user = Permission(
        "Can list Users in Care",
        "",
        PermissionContext.FACILITY,
        [
            ADMIN_ROLE,
            DOCTOR_ROLE,
            NURSE_ROLE,
            GEO_ADMIN,
            STAFF_ROLE,
            FACILITY_ADMIN_ROLE,
            VOLUNTEER_ROLE,
        ],
    )
