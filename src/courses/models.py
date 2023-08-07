from django.db import models

# Create your models here.
from teachers.models import Teacher


class Course(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=100)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name="Profesor",
        default=None,
        null=True,
    )

    class Meta:
        db_table = "Course"

    def __str__(self):
        return self.name or ""
