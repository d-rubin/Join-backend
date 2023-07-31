from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdateDestroySerializer:
    pass


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    
    def get_serializer_class(self):
        # Überschreibe die Methode, um die Serializer-Klasse basierend auf der Aktion zu wählen
        if self.request.method == 'GET':
            return TaskSerializer
        elif self.request.method in ['PATCH', 'DELETE']:
            return TaskUpdateDestroySerializer  # Hier musst du eine entsprechende Serializer-Klasse erstellen
        return TaskSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(assignee=request.user)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        task_id = kwargs['pk']
        task = get_object_or_404(self.queryset, id=task_id)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        task_id = kwargs['pk']
        task = get_object_or_404(self.queryset, id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
