# Generated by Django 5.0 on 2023-12-30 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 30, 10, 51, 46, 993599, tzinfo=datetime.timezone.utc)),
        ),
    ]
