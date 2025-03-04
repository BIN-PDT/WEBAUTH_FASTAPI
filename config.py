from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # GENERAL.
    SECRET_KEY: str
    # DATABASE.
    DATABASE_URL: str
    # JWT.
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRY: int = 3600
    REFRESH_TOKEN_EXPIRY: int = 172800
    # MAIL.
    MAIL_ADDRESS: str
    MAIL_PASSWORD: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM_NAME: str = "FastAPI"

    model_config = SettingsConfigDict(env_file=".env", extra="forbid")


settings = Settings()
