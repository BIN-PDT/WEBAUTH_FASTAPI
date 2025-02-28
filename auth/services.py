from sqlmodel import Session, select
from .models import User
from .schemas import UserCreate
from .utils import get_password_hash


class UserService:
    def get_by_username(self, session: Session, username: str):
        statement = select(User).where(User.username == username)

        result = session.exec(statement)
        user = result.first()
        return user

    def get_by_email(self, session: Session, email: str):
        statement = select(User).where(User.email == email)

        result = session.exec(statement)
        user = result.first()
        return user

    def create(self, session: Session, data: UserCreate):
        hashed_password = get_password_hash(data.password)
        user = User.model_validate(data, update={"password": hashed_password})

        session.add(user)
        session.commit()
        session.refresh(user)
        return user
