from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated


from .models import Task, Subtask
from .serializers import TaskSerializer, SubtaskSerializer


class SubtaskCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubtaskSerializer


class SubTasksList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubtaskSerializer

    def get_queryset(self):
        return Subtask.objects.all()


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

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        subtasks = request.data["subtasks"]
        if subtasks:
            for subtask in subtasks:
                Subtask.create(task=subtask.task, label=subtask.label, is_done=subtask.is_done);


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = SubtaskSerializer
