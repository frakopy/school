from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    name = models.CharField(verbose_name="Nombre Completo", max_length=100)
    employee_id = models.CharField(verbose_name="ID Empleado", max_length=10)
    email = models.CharField(verbose_name="Correo Electrónico", max_length=50)
    phone = models.CharField(verbose_name="Teléfono / Celular", max_length=12)
    rut = models.CharField(verbose_name="Rut", max_length=10, default=None)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name="user_teacher",
        default=None,
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        db_table = "Teachers"

    def __str__(self):
        return self.name or ""
