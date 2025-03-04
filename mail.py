from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from config import settings


config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_ADDRESS,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    MAIL_FROM=settings.MAIL_ADDRESS,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
)


mail = FastMail(config)


async def send_message(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html,
    )
    await mail.send_message(message)


async def send_verification_message(email: str, verification_link: str):
    html_message = f"""
        <div style="font-style: italic;">
            <p>Welcome! We are sending this email to notify you about an important event.</p>
            <p>Please click the <a href="{ verification_link }">link</a> to verify your account.</p>
            <p>Best regards,<br>FastAPI</p>
        </div>
    """
    await send_message(
        recipients=[email],
        subject="Account Verification",
        body=html_message,
    )
