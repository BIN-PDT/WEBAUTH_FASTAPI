from sqlmodel import Session, select
from models.user import User
from schemas.user_schemas import UserCreate, UserUpdate
from utils.password import hash_password


class UserService:
    @staticmethod
    def find_by_id(session: Session, id: int) -> User | None:
        statement = select(User).where(User.id == id)

        result = session.exec(statement)
        user = result.first()
        return user

    @staticmethod
    def find_by_username(session: Session, username: str) -> User | None:
        statement = select(User).where(User.username == username)

        result = session.exec(statement)
        user = result.first()
        return user

    @staticmethod
    def find_by_email(session: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        result = session.exec(statement)
        user = result.first()
        return user

    @staticmethod
    def create(session: Session, data: UserCreate) -> User | None:
        hashed_password = hash_password(data.password)
        user = User.model_validate(data, update={"password": hashed_password})

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update(session: Session, db_user: User, data: UserUpdate):
        update_data = data.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(update_data)

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
