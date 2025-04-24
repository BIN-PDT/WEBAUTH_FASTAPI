from celery import Celery
from src.config.settings import settings


app = Celery(broker=settings.REDIS_URL, backend=settings.REDIS_URL)
app.autodiscover_tasks(["src.celery_tasks"])
