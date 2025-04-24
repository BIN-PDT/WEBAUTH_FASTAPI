from sqlmodel import SQLModel


class ChangePasswordSchema(SQLModel):
    old_password: str
    password: str
    password2: str
