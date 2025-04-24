from typing import Annotated
from fastapi import Depends
from src.exceptions.user_exceptions import UserNotFoundException
from src.database.main import DatabaseSession
from src.models.user import User
from src.services.user_service import UserService
from src.dependencies.jwt_validators import AccessTokenValidator


def get_current_user(session: DatabaseSession, payload: AccessTokenValidator):
    user = UserService.find_by_id(session, payload["sub"])
    if not user:
        raise UserNotFoundException()
    return user


CurrentUserValidator = Annotated[User, Depends(get_current_user)]
