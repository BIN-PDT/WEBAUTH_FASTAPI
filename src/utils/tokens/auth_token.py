from uuid import uuid4
from datetime import datetime, timezone, timedelta
import jwt
from src.config.settings import settings
from src.models.user import User


def create_token(payload: dict, type: str, expiry: timedelta):
    payload.update({"type": type, "exp": datetime.now(timezone.utc) + expiry})
    return jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_auth_token(payload: dict, type: str) -> str:
    expiry = timedelta(
        seconds=(
            settings.REFRESH_TOKEN_EXPIRY
            if type == "access"
            else settings.ACCESS_TOKEN_EXPIRY
        )
    )
    return create_token(payload, type, expiry)


def create_auth_token_pair(user: User) -> dict:
    payload = {"jti": str(uuid4()), "sub": user.id}
    return {
        "access_token": create_auth_token(payload.copy(), "access"),
        "refresh_token": create_auth_token(payload.copy(), "refresh"),
    }


def decode_auth_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_sub": False},
        )
    except:
        return None
