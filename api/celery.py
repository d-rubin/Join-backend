from __future__ import absolute_import, unicode_literals
import os

# from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

from celery import Celery


app = Celery('celery_app',)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
