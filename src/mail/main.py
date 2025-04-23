from fastapi_mail import MessageSchema, MessageType
from .config import mail


def create_message(recipients: list[str], subject: str, context: dict) -> MessageSchema:
    return MessageSchema(
        recipients=recipients,
        subject=subject,
        template_body=context,
        subtype=MessageType.html,
    )


async def send_message(message: MessageSchema, template_name: str) -> None:
    await mail.send_message(message, template_name)
