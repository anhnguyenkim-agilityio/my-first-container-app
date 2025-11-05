from django.urls import path

from .views import HealthCheckView, TaskCreateView, TaskStatusView

urlpatterns = [
    path("tasks/", TaskCreateView.as_view(), name="task-create"),
    path("healthz/", HealthCheckView.as_view(), name="health-check"),
    path("tasks/<str:task_id>/", TaskStatusView.as_view(), name="task-status"),
]
