from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from datetime import datetime, timezone
from abc import ABCMeta, abstractmethod
from typing import Annotated
from database import DatabaseSession
from errors import (
    InvalidTokenError,
    AccessTokenRequiredError,
    RefreshTokenRequiredError,
    InsufficientPermissionError,
)
from utils import SingletonPattern
from .models import RoleEnum, User
from .services import UserService
from .utils import decode_token


class TokenBearer(SingletonPattern, HTTPBearer, metaclass=ABCMeta):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)

        token_data = decode_token(creds.credentials)
        if token_data is None or not self.validate_token(token_data):
            raise InvalidTokenError()
        self.verify_token(token_data)

        return token_data

    def validate_token(self, token_data: dict) -> bool:
        expiry_timestamp = datetime.fromtimestamp(token_data["exp"], timezone.utc)
        if expiry_timestamp < datetime.now(timezone.utc):
            return False
        return True

    @abstractmethod
    def verify_token(self, token_data: dict) -> None: ...


class AccessTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:
        if token_data["refresh"]:
            raise AccessTokenRequiredError()


class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:
        if not token_data["refresh"]:
            raise RefreshTokenRequiredError()


AccessTokenRequired = Annotated[dict, Depends(AccessTokenBearer())]
RefreshTokenRequired = Annotated[dict, Depends(RefreshTokenBearer())]


def get_current_user(session: DatabaseSession, token_data: AccessTokenRequired):
    user_id = token_data["user"]["id"]
    user = UserService().get_by_id(session, user_id)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


class RoleChecker:
    def __init__(self, allowed_roles: list[RoleEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrentUser):
        if user.role not in self.allowed_roles:
            raise InsufficientPermissionError()


OnlyAdmin = Depends(RoleChecker([RoleEnum.ADMIN]))
OnlyUser = Depends(RoleChecker([RoleEnum.USER]))
AllowAdminUser = Depends(RoleChecker([RoleEnum.ADMIN, RoleEnum.USER]))
