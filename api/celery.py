import os
from celery import Celery
from celery.schedules import crontab
from tasks.tasks import send_task_reminder

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('join-backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django apps.
# app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour="8"),
        send_task_reminder.s(),
    )


