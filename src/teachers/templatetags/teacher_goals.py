from django import template
from goals.models import Goals

register = template.Library()


@register.simple_tag
def teacher_goals(user):
    teacher = user.user_teacher
    goals = Goals.objects.filter(teacher=teacher)
    return goals
