from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime


class UserPublic(SQLModel):
    id: int
    username: str
    email: str
    is_verified: bool
    is_active: bool
    date_joined: datetime


class UserCreate(SQLModel):
    username: str = Field(
        max_length=150, schema_extra={"pattern": "^[a-zA-Z0-9_@+.-]+$"}
    )
    password: str = Field(max_length=150)
    email: EmailStr = Field(max_length=150)


class UserLogin(SQLModel):
    username: str
    password: str
