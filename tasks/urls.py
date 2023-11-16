from django.urls import path
from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView, SubtaskCreateAPIView, SubtaskListForTaskAPIView, \
    SubTasksList

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:task_id>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-retrieve-update-destroy'),
    path("<int:task_id>/subtasks/", SubtaskListForTaskAPIView.as_view(), name='Subtasks for Task'),
    path("subtasks/create/", SubtaskCreateAPIView.as_view(), name="Create Subtask"),
    path("subtasks/", SubTasksList.as_view(), name="All Subtasks"),
    path("subtasks/<int:subTask_id>", TaskRetrieveUpdateDestroyView.as_view(), name='Subtask-retrieve-update-destroy')
]
