import time

from celery import Celery
from settings import (
    BROKER_URL,
    CELERY_BROKER_TRANSPORT_OPTIONS,
    CELERY_RESULT_BACKEND,
)

celery = Celery(
    __name__,
    backend=CELERY_RESULT_BACKEND,
    broker=BROKER_URL,
    broker_transport_options=CELERY_BROKER_TRANSPORT_OPTIONS,
    task_create_missing_queues=False,
)


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
