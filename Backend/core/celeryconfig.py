from .config import settings

broker_url = settings.REDIS_URL
result_backend = settings.CELERY_URL

timezone = "Europe/Moscow"
task_serializer = "json"
result_serializer = "json"
accept_contet = ["json"]
