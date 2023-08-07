from django.contrib import admin
from students.models import Student


class StudentAdmin(admin.ModelAdmin):

    # Display specific columns to show in the panel
    list_display = ("name", "user", "rut", "show_classrooms", "email", "phone")

    # Search by fields
    search_fields = ('name',)

    def show_classrooms(self, obj):
        return ''.join(obj.classroom.level.short_name+'-'+obj.classroom.code)

    show_classrooms.short_description = 'Classroom'

admin.site.register(Student, StudentAdmin)