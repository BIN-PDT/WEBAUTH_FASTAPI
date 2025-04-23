from pathlib import Path
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="forbid")

    # GENERAL.
    SECRET_KEY: str
    # DATABASE.
    DATABASE_URL: str
    # PASSWORD.
    HASH_ALGORITHM: list[str] = ["bcrypt"]
    # JWT.
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRY: int = 3600
    REFRESH_TOKEN_EXPIRY: int = 172800
    # MAIL.
    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM_NAME: str = "FastAPI"
    MAIL_TEMPLATE_FOLDER: Path = (
        Path(__file__).resolve().parent.parent / "mail/templates"
    )
    VERIFY_EMAIL_TOKEN_EXPIRY: int = 900
    RESET_PASSWORD_TOKEN_EXPIRY: int = 900


settings = Settings()
