from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, SubtaskCreateAPIView, SubtaskListForTaskAPIView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:task_id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path("subtasks/<int:task_id>", SubtaskListForTaskAPIView.as_view(), name='Subtasks'),
    path("subtasks/create/<int:task_id>", SubtaskCreateAPIView.as_view(), name="Create Subtask"),
]
