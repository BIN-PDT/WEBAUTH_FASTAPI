from fastapi import Request, BackgroundTasks
from src.mail.main import create_message, send_message
from src.utils.tokens.mail_token import create_mail_token


def create_verification_link(email: str, url_name: str, request: Request) -> str:
    token = create_mail_token({"email": email})
    return str(request.url_for(url_name, token=token))


def send_verify_email_message(
    email: str, request: Request, background_tasks: BackgroundTasks
) -> None:
    context = {"link": create_verification_link(email, "verify_email", request)}
    message = create_message([email], "Verify Email", context)
    background_tasks.add_task(send_message, message, "verify_email.html")


def send_reset_password_message(
    email: str, request: Request, background_tasks: BackgroundTasks
) -> None:
    context = {"link": create_verification_link(email, "reset_password", request)}
    message = create_message([email], "Reset Password", context)
    background_tasks.add_task(send_message, message, "reset_password.html")
