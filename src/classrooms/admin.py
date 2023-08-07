from unicodedata import numeric
from django.contrib import admin
from classrooms.models import Classroom, Level, Schedule
from django.utils.safestring import mark_safe
from django.db.models.functions import Concat
from django.db.models import Value
from django.db.models import Q


class ScheduleAdmin(admin.ModelAdmin):
    # Display specific columns to show in the panel
    list_display = ("classroom", "day", "hour", "hour_block")

    # Search by some fields
    search_fields = ("day", "hour", "hour_block")

    def get_search_results(self, request, queryset, search_term):
        if search_term:
            try:
                search_term = int(search_term)
                queryset = queryset.filter(hour_block=search_term)
                return queryset, False
            except:
                queryset = queryset.annotate(
                    classroom_str=Concat(
                        "classroom__level__short_name", Value("-"), "classroom__code"
                    )
                ).filter(Q(classroom_str__icontains=search_term) | Q(day__icontains=search_term))
                return queryset, False
            
        return super().get_search_results(request, queryset, search_term)

class LevelAdmin(admin.ModelAdmin):
    # Display specific columns to show in the panel
    list_display = ("name", "short_name", "availability")


class ClassroomAdmin(admin.ModelAdmin):
    # Display specific columns to show in the panel
    list_display = ("code", "level", "show_teacher")

    def show_teacher(self, obj):
        teachers = [teacher.name for teacher in obj.teacher.all()]
        teachers_html = "<br>".join(teachers)
        return mark_safe(teachers_html)

    show_teacher.short_description = "Profesores"


admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Classroom, ClassroomAdmin)
