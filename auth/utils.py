from passlib.context import CryptContext
import jwt
from datetime import datetime, timezone, timedelta
from config import settings


pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_token(data: dict, is_refresh: bool = False):
    payload = {}
    payload["user"] = data
    payload["refresh"] = is_refresh
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        seconds=(
            settings.REFRESH_TOKEN_EXPIRY
            if is_refresh
            else settings.ACCESS_TOKEN_EXPIRY
        )
    )

    token = jwt.encode(
        payload,
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return token


def decode_token(token: str) -> dict:
    try:
        data = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return data
    except:
        return None
