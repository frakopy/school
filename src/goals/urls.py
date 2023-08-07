from django.urls import path
from .views import (
    GoalCreateView,
    GoalProgressView,
    ProgressSaveView,
    GoalUpdateView,
    GoalDeleteView,
)

urlpatterns = [
    path("create_goal/", GoalCreateView.as_view(), name="create_goal"),
    path("update_goal/<int:pk>", GoalUpdateView.as_view(), name="update_goal"),
    path("delete_goal/<int:pk>", GoalDeleteView.as_view(), name="delete_goal"),
    path("goal_progress/<int:goal_id>", GoalProgressView.as_view(), name="goal_progress"),
    path("goal_progress_save/", ProgressSaveView.as_view(), name="goal_progress_save"),
]
