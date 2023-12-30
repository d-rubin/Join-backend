# Django starts so that shared_task will use this app.
import os
from celery import Celery
from celery.schedules import crontab
# from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils import timezone
# from dotenv import load_dotenv

# from tasks.models import Task

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('join-backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from tasks.tasks import send_task_reminder
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        # crontab(hour="8"),
        crontab(minute='*/5'),
        send_task_reminder.s(),
    )
