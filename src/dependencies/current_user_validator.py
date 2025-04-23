from typing import Annotated
from fastapi import Depends
from exceptions.user_exceptions import UserNotFoundException
from database.main import DatabaseSession
from models.user import User
from services.user_service import UserService
from .jwt_validators import AccessTokenValidator


def get_current_user(session: DatabaseSession, payload: AccessTokenValidator):
    user = UserService.find_by_id(session, payload["sub"])
    if not user:
        raise UserNotFoundException()
    return user


CurrentUserValidator = Annotated[User, Depends(get_current_user)]
