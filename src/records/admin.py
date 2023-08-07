from django.contrib import admin
from .models import Record


class RecordAdmin(admin.ModelAdmin):

    search_fields = ('student__name', 'course__name')

    list_display = (
        "show_student_name",
        "show_classroom",
        "start_date",
        "show_hour",
        "course",
        "present",
        "comments",
        "created",
        "updated"
    )
    readonly_fields = ("created", "updated")

    list_editable = ['present']

    def show_hour(self, obj):
        return obj.schedule.hour

    show_hour.short_description = 'Hora'

    def show_classroom(self, obj):
        return obj.schedule.classroom

    show_classroom.short_description = 'Classroom'

    def show_student_name(self, obj):
        return obj.student.name

    show_student_name.short_description = 'Nombre del Alumno'


admin.site.register(Record, RecordAdmin)
