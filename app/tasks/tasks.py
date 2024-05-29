import asyncio

from app.tasks.async_tasks import refresh_car_location
from app.tasks.celery_conf import celery_app


@celery_app.task(name="refresh_car_location")
def refresh_car_location_task():
    asyncio.run(refresh_car_location())
