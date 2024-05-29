import os

from celery import Celery
from celery.schedules import crontab

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

celery_app = Celery(
    "tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}",
    include=["app.tasks.tasks"]
)

celery_app.conf.beat_schedule = {
    "refresh_car_location": {
        "task": "refresh_car_location",
        "schedule": crontab(minute="*/3")
    }
}
