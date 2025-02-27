from sqlmodel import SQLModel, Field, String
from datetime import datetime, timezone


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(sa_type=String(150))
    password: str = Field(sa_type=String(150))
    email: str = Field(sa_type=String(150))
    is_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    date_joined: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
