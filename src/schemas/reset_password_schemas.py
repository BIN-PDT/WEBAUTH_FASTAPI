from sqlmodel import SQLModel
from pydantic import EmailStr


class PasswordResetRequestSchema(SQLModel):
    email: EmailStr


class PasswordResetConfirmSchema(SQLModel):
    password: str
    password2: str
