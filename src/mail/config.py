from fastapi_mail import FastMail, ConnectionConfig
from src.config.settings import settings

mail = FastMail(
    ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        MAIL_FROM=settings.MAIL_USERNAME,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        TEMPLATE_FOLDER=settings.MAIL_TEMPLATE_FOLDER,
    )
)
