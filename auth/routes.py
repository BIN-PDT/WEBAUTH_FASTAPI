from fastapi import status, APIRouter, HTTPException
from database import DatabaseSession
from .schemas import UserPublic, UserCreate, UserLogin
from .services import UserService
from .dependencies import AccessTokenRequired, RefreshTokenRequired
from .utils import verify_password, create_token


router = APIRouter()


@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_account(data: UserCreate, session: DatabaseSession):
    if UserService().get_by_username(session, data.username):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "User with username already exists",
        )
    if UserService().get_by_email(session, data.email):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "User with email already exists",
        )

    user = UserService().create(session, data)
    return user


@router.post("/signin")
def login(data: UserLogin, session: DatabaseSession):
    user = UserService().get_by_username(session, data.username)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid credentials")

    user_data = {"id": user.id}
    access_token = create_token(user_data)
    refresh_token = create_token(user_data, is_refresh=True)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/refresh_token")
def refresh_token(token_data: RefreshTokenRequired):
    return {"access_token": create_token(token_data["user"])}
