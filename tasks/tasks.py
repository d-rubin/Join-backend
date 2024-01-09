import os

from api.celery import app
from django.contrib.auth.models import User
from django.utils import timezone
from dotenv import load_dotenv
from tasks.models import Task
from django.conf import settings
from django.core.mail import EmailMessage, get_connection


@app.task
def send_task_reminder():
    load_dotenv()
    today = timezone.now()
    tasks = Task.objects.filter(due_date__lte=today)

    for task in tasks:
        user = User.objects.get(username=task.assignee)
        # body = render_to_string('due_task.html', {'name': user.username, "task": task.title}),
        body = f"Hello {user.username},\nthe Task {task.title} is due."
        with get_connection(
                host=settings.RESEND_SMTP_HOST,
                port=settings.RESEND_SMTP_PORT,
                username=settings.RESEND_SMTP_USERNAME,
                password=os.environ["RESEND_API_KEY"],
                use_tls=True,
        ) as connection:
            r = EmailMessage(
                subject="Reminder from Join",
                body=body,
                to=[user.email],
                from_email="join@daniel-rubin.de",
                connection=connection).send()
