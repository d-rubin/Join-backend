from django.template.loader import render_to_string
from django.utils import timezone
from api.celery import app
from tasks.models import Task, StatusChoices
from django.core.mail import send_mail
from django.contrib.auth.models import User


@app.task
def send_task_reminder():
    today = timezone.now()
    tasks = Task.objects.filter(due_date__lte=today, status=not StatusChoices.DONE)
    for task in tasks:
        user = User.objects.get(username=task.assignee)
        send_mail(
            "Reminder",
            'You have a due task',
            "join@daniel-rubin.de",
            [user.email],
            fail_silently=False,
            html_message=render_to_string('due_task.html', {'name': user.username, "task": task}))
