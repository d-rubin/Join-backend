import django
from django.contrib.auth.models import User
from django.db.models import Model, CharField, TextField, DateField, ForeignKey, CASCADE, TextChoices, \
    BooleanField


class CategoryChoices(TextChoices):
    BACKOFFICE = "backoffice", "Backoffice"
    DESIGN = "design", "Design"
    MARKETING = "marketing", "Marketing"
    SALES = "sales", "Sales"
    MEDIA = "media", "Media"


class PriorityChoices(TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"


class StatusChoices(TextChoices):
    IN_PROGRESS = "inProgress", "In progress"
    TO_DO = "toDo", "To-do"
    AWAITING_FEEDBACK = "awaitingFeedback", "Awaiting feedback"
    DONE = "done", "Done"


class Task(Model):
    title = CharField(max_length=30)
    description = TextField(max_length=100)
    due_date = DateField(default=django.utils.timezone.now)
    category = CharField(max_length=20, choices=CategoryChoices.choices, default=CategoryChoices.DESIGN)
    priority = CharField(max_length=20, choices=PriorityChoices.choices, default=PriorityChoices.LOW)
    status = CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.TO_DO)
    assignee = ForeignKey(
        User,
        on_delete=CASCADE,
        default=1,
    )

    def __str__(self):
        return self.title


class Subtask(Model):
    label = CharField(max_length=50)
    is_done = BooleanField(default=False)
    task = ForeignKey(Task, on_delete=CASCADE, null=True)

    def __str__(self):
        return self.label
