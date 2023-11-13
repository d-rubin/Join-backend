from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, SubtaskCreateAPIView, SubtaskListForTaskAPIView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:task_id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path("<int:task_id>/subtasks/", SubtaskListForTaskAPIView.as_view(), name='Subtasks'),
    path("subtasks/create/", SubtaskCreateAPIView.as_view(), name="Create Subtask"),
]
