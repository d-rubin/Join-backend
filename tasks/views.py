from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Task, Subtask
from .serializers import TaskSerializer, SubtaskSerializer


class SubtaskCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubtaskSerializer

    def post(self, request, *args, **kwargs):
        task_id = self.kwargs['task_id']
        task = Task.objects.get(id=task_id)

        request.data["task_id"] = task.id

        return self.create(request, *args, **kwargs)


class SubtaskListForTaskAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubtaskSerializer

    def get_queryset(self):
        return Subtask.objects.filter(task_id=self.kwargs['task_id'])


class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_url_kwarg = "task_id"
    lookup_field = "id"
    serializer_class = TaskSerializer
