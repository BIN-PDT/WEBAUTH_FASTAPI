from sqlmodel import SQLModel


class ChangeEmailSchema(SQLModel):
    email: str
