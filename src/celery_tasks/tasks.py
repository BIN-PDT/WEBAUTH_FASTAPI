from asgiref.sync import async_to_sync
from src.celery_tasks.config import app
from src.mail.main import create_message, send_message


@app.task()
def send_verify_email_message_task(email: str, link: str) -> None:
    message = create_message([email], "Verify Email", {"link": link})
    async_to_sync(send_message)(message, "verify_email.html")


@app.task()
def send_reset_password_message_task(email: str, link: str) -> None:
    message = create_message([email], "Reset Password", {"link": link})
    async_to_sync(send_message)(message, "reset_password.html")
