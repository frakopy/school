from django.contrib import admin
from teachers.models import Teacher


class TeacherAdmin(admin.ModelAdmin):

    # Display specific columns to show in the panel
    list_display = ("name", "user", "employee_id", "email", "phone", "rut")

    # Search using 'name' field
    search_fields = ["name"]


admin.site.register(Teacher, TeacherAdmin)
