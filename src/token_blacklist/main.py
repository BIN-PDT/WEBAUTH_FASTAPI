from .config import redis_client


def revoke_token(token_id: str, ttl: int):
    redis_client.setex(token_id, ttl, "")


def check_revoked_token(token_id: str):
    return redis_client.get(token_id) is not None
