from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from src.database.config import engine


def get_session():
    with Session(
        engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    ) as session:
        yield session


DatabaseSession = Annotated[Session, Depends(get_session)]
