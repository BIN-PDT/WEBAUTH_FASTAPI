from .config import crypt_context


def hash_password(password: str) -> str:
    return crypt_context.hash(password)


def verify_password(plain: str, hash: str) -> bool | None:
    try:
        return crypt_context.verify(plain, hash)
    except:
        return None
