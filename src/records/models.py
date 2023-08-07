from django.db import models
from classrooms.models import Schedule
from students.models import Student
from courses.models import Course


class Record(models.Model):
    student = models.ForeignKey(
        Student,
        related_name="record_student",
        verbose_name="Estudiante",
        on_delete=models.CASCADE,
    )
    schedule = models.ForeignKey(
        Schedule,
        related_name="schedule_student",
        verbose_name="Programación",
        on_delete=models.CASCADE,
        null=False,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="record_course",
        verbose_name="Asignatura",
        null=False,
    )
    present = models.BooleanField(
        default=None, null=True,
        verbose_name="Presente"
    )
    comments = models.CharField(
        verbose_name="Observaciones",
        max_length=255,
        blank=True,
        null=True,
        default=" "
    )

    start_date = models.DateField(verbose_name="Fecha De Inicio")

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Record"
        db_table = "Record"

    def __str__(self):
        return f"{self.student} en {self.schedule}"
