from fakeredis import FakeRedis
from redis import Redis
from src.config.settings import settings


redis_client = (
    FakeRedis() if settings.REDIS_URL is None else Redis.from_url(settings.REDIS_URL)
)
