from fastapi import Depends
from sqlmodel import create_engine, Session
from typing import Annotated
from config import settings


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)


def get_session():
    with Session(
        engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    ) as session:
        yield session


DatabaseSession = Annotated[Session, Depends(get_session)]
