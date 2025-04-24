from fastapi import Depends
from src.exceptions.auth_exceptions import InsufficientPermissionException
from src.models.user import RoleEnum
from src.dependencies.current_user_validator import CurrentUserValidator


class RoleChecker:
    def __init__(self, allowed_roles: list[RoleEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrentUserValidator):
        if user.role not in self.allowed_roles:
            raise InsufficientPermissionException()


OnlyAdminValidator = Depends(RoleChecker([RoleEnum.ADMIN]))
OnlyUserValidator = Depends(RoleChecker([RoleEnum.USER]))
AllowAdminUserValidator = Depends(RoleChecker([RoleEnum.ADMIN, RoleEnum.USER]))
