from fastapi import status, APIRouter, Request, BackgroundTasks
from config import settings
from database import DatabaseSession
from mail import send_email_verification_message, send_password_reset_message
from errors import (
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
    NewPasswordMismatchConfirmPasswordError,
)
from .schemas import (
    UserCreate,
    UserUpdate,
    UserLogin,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from .services import UserService
from .dependencies import AccessTokenRequired, RefreshTokenRequired
from .utils import (
    get_password_hash,
    verify_password,
    create_jwt_token,
    create_url_safe_token,
    decode_url_safe_token,
)


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_account(
    request: Request,
    data: UserCreate,
    session: DatabaseSession,
    background_tasks: BackgroundTasks,
):
    if UserService().get_by_username(session, data.username):
        raise UsernameAlreadyExistsError()
    if UserService().get_by_email(session, data.email):
        raise EmailAlreadyExistsError()

    user = UserService().create(session, data)

    token = create_url_safe_token({"email": user.email})
    verification_link = request.url_for("verify_email", token=token)
    background_tasks.add_task(
        send_email_verification_message, user.email, verification_link
    )

    return {
        "message": "Signed up successfully! Please check email to verify your account",
        "user": user,
    }


@router.get("/verify/{token}", name="verify_email")
def verify_email_account(token: str, session: DatabaseSession):
    token_data = decode_url_safe_token(token, settings.EMAIL_VERIFICATION_TOKEN_EXPIRY)
    if token_data is None:
        raise InvalidTokenError()
    user_email = token_data.get("email")
    if user_email is None:
        raise InvalidTokenError()
    user = UserService().get_by_email(session, user_email)
    if user is None:
        raise UserNotFoundError()

    update_data = UserUpdate(is_verified=True)
    UserService().update(session, user, update_data)

    return {"message": "Account verified successfully"}


@router.post("/signin")
def login(data: UserLogin, session: DatabaseSession):
    user = UserService().get_by_username(session, data.username)

    if not user or not verify_password(data.password, user.password):
        raise InvalidCredentialsError()

    user_data = {"id": user.id}
    access_token = create_jwt_token(user_data)
    refresh_token = create_jwt_token(user_data, is_refresh=True)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/refresh_token")
def refresh_token(token_data: RefreshTokenRequired):
    return {"access_token": create_jwt_token(token_data["user"])}


@router.get("/logout")
def logout(token_data: AccessTokenRequired):
    # REVOKE TOKEN HERE.
    return {"message": "Logged out successfully"}


@router.post("/request_password_reset")
async def request_password_reset(
    data: PasswordResetRequest,
    background_tasks: BackgroundTasks,
):
    # LINK TO CONFIRM PASSWORD RESET INTERFACE.
    token = create_url_safe_token({"email": data.email})
    verification_link = f".../{token}"
    background_tasks.add_task(
        send_password_reset_message, data.email, verification_link
    )

    return {
        "message": "Requested successfully! Please check email to reset your account password"
    }


@router.post("/reset_password/{token}")
def reset_password(token: str, data: PasswordResetConfirm, session: DatabaseSession):
    token_data = decode_url_safe_token(token, settings.PASSWORD_RESET_TOKEN_EXPIRY)
    if token_data is None:
        raise InvalidTokenError()
    user_email = token_data.get("email")
    if user_email is None:
        raise InvalidTokenError()
    if data.new_password != data.confirm_password:
        raise NewPasswordMismatchConfirmPasswordError()
    user = UserService().get_by_email(session, user_email)
    if user is None:
        raise UserNotFoundError()

    hashed_password = get_password_hash(data.new_password)
    update_data = UserUpdate(password=hashed_password)
    UserService().update(session, user, update_data)

    return {"message": "Account password reset successfully"}
