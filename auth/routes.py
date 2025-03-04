from fastapi import status, APIRouter, Request
from database import DatabaseSession
from mail import send_verification_message
from errors import (
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    UserNotFoundError,
)
from .schemas import UserCreate, UserUpdate, UserLogin
from .services import UserService
from .dependencies import AccessTokenRequired, RefreshTokenRequired
from .utils import (
    verify_password,
    create_jwt_token,
    create_url_safe_token,
    decode_url_safe_token,
)


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_account(request: Request, data: UserCreate, session: DatabaseSession):
    if UserService().get_by_username(session, data.username):
        raise UsernameAlreadyExistsError()
    if UserService().get_by_email(session, data.email):
        raise EmailAlreadyExistsError()

    user = UserService().create(session, data)

    token = create_url_safe_token({"email": user.email})
    verification_link = request.url_for("verify_email", token=token)
    await send_verification_message(user.email, verification_link)

    return {
        "message": "Signed up successfully! Please check email to verify your account",
        "user": user,
    }


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


@router.get("/verify/{token}", name="verify_email")
def verify_email_account(token: str, session: DatabaseSession):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")
    if user_email is None:
        raise InvalidTokenError()
    user = UserService().get_by_email(session, user_email)
    if user is None:
        raise UserNotFoundError()

    update_data = UserUpdate(is_verified=True)
    UserService().update(session, user, update_data)

    return {"message": "Account verified successfully"}
