import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "postcredit.settings")

app = Celery("postcredit")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    "send-daily-report": {
        "task": "api.tasks.send_daily_report",
        "schedule": crontab(hour=9, minute=0),  # Every day at 9 AM
    },
    "cleanup-old-data": {
        "task": "api.tasks.cleanup_old_data",
        "schedule": crontab(hour=2, minute=0),  # Every day at 2 AM
    },
    "health-check-every-5-minutes": {
        "task": "api.tasks.health_check",
        "schedule": 10.0,  # Every 5 minutes (in seconds)
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
