from rest_framework.serializers import ModelSerializer

from .models import Task, Subtask


class SubtaskSerializer(ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'label', 'is_done']


class TaskSerializer(ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'category', 'priority', 'status', 'assignee', 'subtasks']
