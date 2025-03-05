from passlib.context import CryptContext
import jwt
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timezone, timedelta
from config import settings


pwd_context = CryptContext(schemes=["bcrypt"])
ust_serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_jwt_token(data: dict, is_refresh: bool = False) -> str:
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


def decode_jwt_token(token: str) -> dict | None:
    try:
        data = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return data
    except:
        return None


def create_url_safe_token(data: dict) -> str:
    return ust_serializer.dumps(data)


def decode_url_safe_token(token: str) -> dict | None:
    try:
        data = ust_serializer.loads(
            token,
            max_age=settings.EMAIL_VERIFICATION_TOKEN_EXPIRY,
        )
        return data
    except:
        return None
