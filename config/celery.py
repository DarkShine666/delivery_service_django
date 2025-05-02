import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("delivery_service")
app.conf.broker_url = f"redis://{os.environ.get('REDIS_HOST', 'redis')}:{os.environ.get('REDIS_PORT', 6379)}/0"
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "recalculate_pending_parcels": {
        "task": "parcels.tasks.recalculate_pending_parcels",
        "schedule": crontab(minute="*/5"),
    },
}
