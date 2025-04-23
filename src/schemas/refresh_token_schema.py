from sqlmodel import SQLModel


class RefreshTokenSchema(SQLModel):
    refresh_token: str
