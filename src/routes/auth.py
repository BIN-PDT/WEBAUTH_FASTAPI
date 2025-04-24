from typing import Annotated
from fastapi import APIRouter, status, Request, BackgroundTasks
from fastapi import Body, Path
from src.config.settings import settings
from src.exceptions.auth_exceptions import (
    InvalidTokenException,
    InvalidLoginCredentialsException,
)
from src.exceptions.user_exceptions import (
    DuplicateUsernameException,
    DuplicateEmailException,
    VerifiedEmailException,
    WrongPasswordException,
    UserNotFoundException,
    ConfirmPasswordMismatchException,
)
from src.database.main import DatabaseSession
from src.token_blacklist.main import revoke_token, check_revoked_token
from src.schemas.api_response import APIResponse
from src.schemas.user_schemas import UserPublic, UserCreate, UserUpdate
from src.schemas.signin_schema import SignInSchema
from src.schemas.reset_password_schemas import (
    PasswordResetRequestSchema,
    PasswordResetConfirmSchema,
)
from src.schemas.refresh_token_schema import RefreshTokenSchema
from src.schemas.change_email_schema import ChangeEmailSchema
from src.schemas.change_password_schema import ChangePasswordSchema
from src.services.user_service import UserService
from src.dependencies.jwt_validators import AccessTokenValidator
from src.dependencies.current_user_validator import CurrentUserValidator
from src.utils.password import hash_password, verify_password
from src.utils.mail import (
    create_verification_link,
    send_verify_email_message,
    send_reset_password_message,
)
from src.utils.tokens.mail_token import decode_mail_token
from src.utils.tokens.auth_token import create_auth_token_pair, decode_auth_token
from src.celery_tasks.tasks import (
    send_verify_email_message_task,
    send_reset_password_message_task,
)


router = APIRouter()


@router.post("/signup")
def signup(
    request: Request,
    data: Annotated[UserCreate, Body()],
    session: DatabaseSession,
    background_tasks: BackgroundTasks,
):
    if UserService.find_by_username(session, data.username):
        raise DuplicateUsernameException()
    if UserService.find_by_email(session, data.email):
        raise DuplicateEmailException()

    user = UserService.create(session, data)

    if settings.REDIS_URL is None:
        send_verify_email_message(user.email, request, background_tasks)
    else:
        link = create_verification_link(user.email, "verify_email", request)
        send_verify_email_message_task.delay(user.email, link)

    return APIResponse(
        status_code=status.HTTP_201_CREATED,
        message="Signed up successfully.",
        data=UserPublic(**user.model_dump()),
    )


@router.get("/verify-email/{token}", name="verify_email")
def verify_email(token: Annotated[str, Path()], session: DatabaseSession):
    payload = decode_mail_token(token, settings.VERIFY_EMAIL_TOKEN_EXPIRY)
    if payload is None or check_revoked_token(payload["mti"]):
        raise InvalidTokenException()
    email = payload.get("email")
    if email is None:
        raise InvalidTokenException()
    user = UserService.find_by_email(session, email)
    if user is None:
        raise UserNotFoundException()

    data = UserUpdate(is_verified=True)
    UserService.update(session, user, data)

    revoke_token(payload["mti"], settings.VERIFY_EMAIL_TOKEN_EXPIRY)

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Verified email successfully.",
    )


@router.post("/signin")
def signin(data: Annotated[SignInSchema, Body()], session: DatabaseSession):
    user = UserService.find_by_username(session, data.username)

    if not user or not verify_password(data.password, user.password):
        raise InvalidLoginCredentialsException()

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Signed in successfully.",
        data={**create_auth_token_pair(user), "user": UserPublic(**user.model_dump())},
    )


@router.post("/reset-password")
async def request_password_reset(
    request: Request,
    data: Annotated[PasswordResetRequestSchema, Body()],
    session: DatabaseSession,
    background_tasks: BackgroundTasks,
):
    user = UserService.find_by_email(session, data.email)
    if user:
        if settings.REDIS_URL is None:
            send_reset_password_message(user.email, request, background_tasks)
        else:
            link = create_verification_link(user.email, "reset_password", request)
            send_reset_password_message_task.delay(user.email, link)

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Requested reset password successfully.",
    )


@router.patch("/reset-password/{token}", name="reset_password")
def confirm_password_reset(
    token: Annotated[str, Path()],
    data: Annotated[PasswordResetConfirmSchema, Body()],
    session: DatabaseSession,
):
    payload = decode_mail_token(token, settings.RESET_PASSWORD_TOKEN_EXPIRY)
    if payload is None or check_revoked_token(payload["mti"]):
        raise InvalidTokenException()
    email = payload.get("email")
    if email is None:
        raise InvalidTokenException()
    if data.password != data.password2:
        raise ConfirmPasswordMismatchException()
    user = UserService.find_by_email(session, email)
    if user is None:
        raise UserNotFoundException()

    hashed_password = hash_password(data.password)
    update_data = UserUpdate(password=hashed_password)
    UserService.update(session, user, update_data)

    revoke_token(payload["mti"], settings.RESET_PASSWORD_TOKEN_EXPIRY)

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Confirmed reset password successfully.",
    )


@router.post("/refresh-token")
def refresh_token(
    access_payload: AccessTokenValidator,
    current_user: CurrentUserValidator,
    data: Annotated[RefreshTokenSchema, Body()],
):
    refresh_payload = decode_auth_token(data.refresh_token)
    if refresh_payload is None or (
        refresh_payload["type"] != "refresh"
        or refresh_payload["jti"] != access_payload["jti"]
        or refresh_payload["sub"] != access_payload["sub"]
    ):
        raise InvalidTokenException()

    revoke_token(access_payload["jti"], settings.REFRESH_TOKEN_EXPIRY)

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Refreshed tokens successfully.",
        data={**create_auth_token_pair(current_user)},
    )


@router.patch("/change-email")
def change_email(
    current_user: CurrentUserValidator,
    data: Annotated[ChangeEmailSchema, Body()],
    session: DatabaseSession,
):
    if UserService.find_by_email(session, data.email):
        raise DuplicateEmailException()

    current_user.email = data.email
    current_user.is_verified = False
    session.add(current_user)
    session.commit()

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Changed email successfully.",
    )


@router.get("/send-email-verification")
def send_email_verification(
    request: Request,
    current_user: CurrentUserValidator,
    background_tasks: BackgroundTasks,
):
    if current_user.is_verified:
        raise VerifiedEmailException()

    if settings.REDIS_URL is None:
        send_verify_email_message(current_user.email, request, background_tasks)
    else:
        link = create_verification_link(current_user.email, "verify_email", request)
        send_verify_email_message_task.delay(current_user.email, link)

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Sended email verification successfully.",
    )


@router.patch("/change-password")
def change_password(
    current_user: CurrentUserValidator,
    data: Annotated[ChangePasswordSchema, Body()],
    session: DatabaseSession,
):
    if data.password != data.password2:
        raise ConfirmPasswordMismatchException()
    if not verify_password(data.old_password, current_user.password):
        raise WrongPasswordException()

    current_user.password = hash_password(data.password)
    session.add(current_user)
    session.commit()

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Changed password successfully.",
    )


@router.get("/signout")
def signout(access_payload: AccessTokenValidator):
    revoke_token(access_payload["jti"], settings.REFRESH_TOKEN_EXPIRY)

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Signed out successfully.",
    )


@router.delete("/delete-account")
def delete_account(
    access_payload: AccessTokenValidator,
    current_user: CurrentUserValidator,
    session: DatabaseSession,
):
    session.delete(current_user)
    session.commit()

    revoke_token(access_payload["jti"], settings.REFRESH_TOKEN_EXPIRY)

    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Deleted account successfully.",
    )
