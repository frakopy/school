from django.urls import path
from .views import (
    RecordsView,
    GetJsonProgressView,
    SaveRecordsView,
    TotalRecordsView,
    CreateRecordsStudentView,
    UpdateRecordsView,
    StudentRecordView,
    StudentRecordUpdateView,
    StudentRecordDeleteView,
    StudentScheduleWeekView,
)

urlpatterns = [
    path("<int:classroom_id>/<str:hour_str>/", RecordsView.as_view(), name="records_list"),
    path("get_json_progress/<int:classroom_id>/<str:hour_str>/", GetJsonProgressView.as_view(), name="get_json_progress"),
    path("total_records", TotalRecordsView.as_view(), name="total_records"),
    path("save/<int:classroom_id>/<str:hour_str>/", SaveRecordsView.as_view(), name="save_records"),
    path("create_records_student/", CreateRecordsStudentView.as_view(), name="create_records_student"),
    path("update/<int:pk>", UpdateRecordsView.as_view(), name="update_record"),
    path("student_records/<int:student_id>/<int:teacher_id>", StudentRecordView.as_view(), name="student_records"),
    path("student_record_update/<int:pk>", StudentRecordUpdateView.as_view(), name="student_record_update"),
    path("student_record_delete/<int:pk>", StudentRecordDeleteView.as_view(), name="student_record_delete"),
    path("student_schedule_week/<int:student_id>", StudentScheduleWeekView.as_view(), name="student_schedule_week"),
]
