from datetime import time
from django.db import models
from teachers.models import Teacher


# Create your models here.


class Level(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=100)
    short_name = models.CharField(verbose_name="Abreviación", max_length=10)
    active = models.BooleanField(verbose_name="Activo")
    availability = models.IntegerField(verbose_name="Disponibilidad de cupos", default=0)

    class Meta:
        db_table = "Level"

    def __str__(self):
        return self.name or ""


class Classroom(models.Model):
    code = models.CharField(verbose_name="Letra", max_length=2)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, verbose_name="Clase", default=None, null=True
    )
    teacher = models.ManyToManyField(
        Teacher,
        verbose_name="Profesor Jefe",
        default=None,
    )

    class Meta:
        db_table = "Classroom"

    def __str__(self):
        return f"{self.level.short_name}-{self.code}" or ""


class Schedule(models.Model):
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="classroom_schedule"
    )
    day = models.CharField(
        verbose_name="Día de la semana",
        max_length=9,
        choices=[
            ("Lunes", "Lunes"),
            ("Martes", "Martes"),
            ("Miércoles", "Miércoles"),
            ("Jueves", "Jueves"),
            ("Viernes", "Viernes"),
        ],
    )
    hour = models.TimeField(
        verbose_name="Hora",
        choices=[
            (time(8, 0), "8:00 AM"),
            (time(8, 15), "8:15 AM"),
            (time(9, 0), "9:00 AM"),
            (time(9, 45), "9:45 AM"),
            (time(10, 0), "10:00 AM"),
            (time(10, 45), "10:45 AM"),
            (time(11, 30), "11:30 AM"),
            (time(11, 45), "11:45 AM"),
            (time(12, 30), "12:30 PM"),
            (time(13, 15), "1:15 PM"),
            (time(14, 0), "2:00 PM"),
            (time(14, 45), "2:45 PM"),
            (time(14, 55), "2:55 PM"),
            (time(15, 40), "3:40 PM"),
        ],
    )

    hour_block = models.IntegerField(verbose_name="Bloque de Hora", default=1)

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
        db_table = "Schedule"

    def __str__(self):
        return f"{self.classroom} {self.day} a las {self.hour}"
