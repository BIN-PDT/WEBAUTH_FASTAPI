from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from src.config.settings import settings


crypt_context = CryptContext(schemes=settings.HASH_ALGORITHM)
url_token_serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
