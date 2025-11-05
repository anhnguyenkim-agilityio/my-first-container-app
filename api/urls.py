from django.urls import path

from .views import TaskCreateView, TaskStatusView

urlpatterns = [
    path("tasks/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<str:task_id>/", TaskStatusView.as_view(), name="task-status"),
]
