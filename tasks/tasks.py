from __future__ import absolute_import, unicode_literals
import os

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from dotenv import load_dotenv

from tasks.models import Task


@shared_task
def send_task_reminder():
    load_dotenv()
    today = timezone.now()
    tasks = Task.objects.filter(due_date__lte=today)
    print("Triggered")

    for task in tasks:
        user = User.objects.filter(username=task.assignee)
        send_mail(
            'Reminder',
            f'{task.title} is due today',
            'contact@daniel-rubin.de',
            [user.email],
            fail_silently=True,
            auth_user=os.environ.get('EMAIL_HOST_USER'),
            auth_password=os.environ.get("EMAIL_HOST_PASSWORD"),
            html_message=render_to_string('due_task.html', {'name': user.name, "task": task.title})),
