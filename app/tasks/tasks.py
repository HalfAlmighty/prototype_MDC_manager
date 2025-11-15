#app/tasks.py

from celery import Celery

celery = Celery(
    "mdc_manager",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
