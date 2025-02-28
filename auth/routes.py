from fastapi import status, APIRouter, HTTPException
from database import DatabaseSession
from .schemas import UserPublic, UserCreate
from .services import UserService


router = APIRouter()
user_service = UserService()


@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_account(data: UserCreate, session: DatabaseSession):
    if user_service.get_by_username(session, data.username):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "User with username already exists",
        )
    if user_service.get_by_email(session, data.email):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "User with email already exists",
        )

    user = user_service.create(session, data)
    return user
