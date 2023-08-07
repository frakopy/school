from django.urls import path
from .views import ClassroomListView, UncompletedScheduleView

urlpatterns = [
    path('', ClassroomListView.as_view(), name='home_teachers'),
    path('head_teachers', UncompletedScheduleView.as_view(), name='head_teachers'),
]
