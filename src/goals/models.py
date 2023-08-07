from django.db import models
from courses.models import Course
from students.models import Student
from teachers.models import Teacher
from classrooms.models import Classroom
from django.core.validators import MaxValueValidator, MinValueValidator


class Goals(models.Model):
    name = models.CharField(verbose_name="Objetivo", max_length=250)
    teacher = models.ForeignKey(
        Teacher,
        verbose_name="Profesor",
        on_delete=models.CASCADE,
        related_name="teacher_goals",
    )

    classroom = models.ForeignKey(
        Classroom,
        verbose_name="Classroom",
        on_delete=models.CASCADE,
        related_name="classroom_goals",
    )
    course = models.ForeignKey(
        Course,
        verbose_name="Asignatura",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:

        verbose_name = "Goal"
        verbose_name_plural = "Goals"

    def __str__(self):
        return self.name


class GoalProgress(models.Model):

    progress = models.PositiveSmallIntegerField(
        verbose_name="Avance",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    goals = models.ForeignKey(Goals, on_delete=models.CASCADE, related_name='goal_progress')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_progress')
    comments = models.TextField(
        verbose_name="Observaciones", blank=True, null=True, default=""
    )

    class Meta:
        """Meta definition for GoalProgress."""

        verbose_name = "Goal Progress"
        verbose_name_plural = "Goals Progress"

    def __str__(self):
        return self.goals.name

