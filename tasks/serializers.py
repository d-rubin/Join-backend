from rest_framework.serializers import ModelSerializer

from .models import Task, Subtask


class SubtaskSerializer(ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['label', 'is_done', 'task', 'id']


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'category', 'priority', 'status', 'assignee']
