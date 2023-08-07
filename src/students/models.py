from django.db import models
from classrooms.models import Classroom
from django.contrib.auth.models import User 

# Create your models here.


class Student(models.Model):
    name = models.CharField(verbose_name="Nombre Completo", max_length=100)
    student_id = models.CharField(verbose_name="ID Alumno", max_length=10)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name="student",
        default=None,
        null=True,
        blank=True,
    )
    rut = models.CharField(verbose_name="Rut", max_length=10)
    classroom = models.ForeignKey(
        Classroom,
        verbose_name="Salón De Clase",
        related_name="students",
        on_delete=models.DO_NOTHING,
    )
    email = models.CharField(verbose_name="Correo Electrónico", max_length=50)
    phone = models.CharField(verbose_name="Teléfono / Celular", max_length=12)

    class Meta:
        db_table = "Students"

    def __str__(self):
        return self.name or ""
