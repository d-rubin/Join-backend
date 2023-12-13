from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Task
from django.contrib.auth.models import User



@shared_task
def check_due_dates():
    today = timezone.now().date()
    tasks_due_today = Task.objects.filter(due_date=today)

    for task in tasks_due_today:
        # Sende eine E-Mail für jedes fällige Todo
        subject = f'{task.title}'
        message = f'The Task {task.title} is due today.'
        user = User.objects.find(name=task.assignee)
        send_mail(
            subject,
            message,
            'contact@daniel-rubin.de',
            [user.email],
            fail_silently=True,
            auth_user='m06624d4',
            auth_password='3Y9kJcKSxBPgZp9ZT6aY',
            html_message=render_to_string('due_task.html', {'name': user.name, "task": task.title})),
