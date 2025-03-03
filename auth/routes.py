from fastapi import status, APIRouter, HTTPException
from database import DatabaseSession
from errors import (
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)
from .schemas import UserPublic, UserCreate, UserLogin
from .services import UserService
from .dependencies import AccessTokenRequired, RefreshTokenRequired
from .utils import verify_password, create_token


router = APIRouter()


@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_account(data: UserCreate, session: DatabaseSession):
    if UserService().get_by_username(session, data.username):
        raise UsernameAlreadyExistsError()
    if UserService().get_by_email(session, data.email):
        raise EmailAlreadyExistsError()

    user = UserService().create(session, data)
    return user


@router.post("/signin")
def login(data: UserLogin, session: DatabaseSession):
    user = UserService().get_by_username(session, data.username)

    if not user or not verify_password(data.password, user.password):
        raise InvalidCredentialsError()

    user_data = {"id": user.id}
    access_token = create_token(user_data)
    refresh_token = create_token(user_data, is_refresh=True)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/refresh_token")
def refresh_token(token_data: RefreshTokenRequired):
    return {"access_token": create_token(token_data["user"])}


@router.get("/logout")
def logout(token_data: AccessTokenRequired):
    # REVOKE TOKEN HERE.
    return {"message": "Logged out successfully"}
