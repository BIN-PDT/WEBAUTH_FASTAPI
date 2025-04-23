from sqlmodel import SQLModel


class SignInSchema(SQLModel):
    username: str
    password: str
