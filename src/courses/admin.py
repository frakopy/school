from django.contrib import admin
from courses.models import Course


class CourseAdmin(admin.ModelAdmin):

    # Display specific columns to show in the panel
    list_display = ("name", "teacher", "show_classroom")

    search_fields = ("name", "teacher__name",)

    def show_classroom(self, obj):
        return [classroom for classroom in obj.teacher.classroom_set.all()]

    show_classroom.short_description = "Classrooms"

admin.site.register(Course, CourseAdmin)
