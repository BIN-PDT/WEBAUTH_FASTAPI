from uuid import uuid4
from src.utils.config import url_token_serializer


def create_mail_token(data: dict) -> str:
    data.update({"mti": str(uuid4())})
    return url_token_serializer.dumps(data)


def decode_mail_token(token: str, expiry: int) -> dict | None:
    try:
        return url_token_serializer.loads(token, max_age=expiry)
    except:
        return None
