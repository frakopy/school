from django.contrib import admin
from .models import Goals, GoalProgress


class GoalsAdmin(admin.ModelAdmin):

    # Display specific columns to show in the panel
    list_display = ("name", "teacher", "classroom", "course")


class GoalProgressAdmin(admin.ModelAdmin):

    # Display specific columns to show in the panel
    list_display = ("show_goal_name", "display_progress", "student", "comments")


    def display_progress(self, obj):
        return f"{obj.progress}%"
    display_progress.short_description = "Avance"

    def show_goal_name(self, obj):
        return obj.goals.name
    show_goal_name.short_description = "Nombre del Objetivo"


admin.site.register(Goals, GoalsAdmin)
admin.site.register(GoalProgress, GoalProgressAdmin)
