from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Teacher

# TODO: Utilizar las señales de abajo cuando se tengan las pantallas de creacion de usuario

# @receiver(post_save, sender=User)
# def create_teacher(sender, instance, **kwargs):
#     if kwargs.get('created', False):
#         # Obtén un Teacher existente que cumpla con ciertas condiciones
#         existing_teacher = Teacher.objects.filter(email=instance.email).first()
#         if existing_teacher:
#             # Asigna el Teacher existente al usuario nuevo
#             existing_teacher.user = instance
#             existing_teacher.save()
#         else:
#             # Crea un nuevo Teacher asociado con el usuario nuevo
#             Teacher.objects.create(user=instance, email=instance.email)


# # Señal a ser ejecutada al momento de crear un profesor
# @receiver(pre_save, sender=Teacher)
# def create_teacher(sender, instance, **kwargs):
#     # Se intenta recuperar un profesor en base al email 
#     existing_teacher = Teacher.objects.filter(email=instance.email).first()
    
#     if existing_teacher:
#         # Se actualizan ciertos campos del profesor existente
#         existing_teacher.name = instance.name
#         existing_teacher.employee_id = instance.employee_id
#         existing_teacher.phone = instance.phone
#         existing_teacher.rut = instance.rut
#         existing_teacher.save()

#         # Anula el guardado de la nueva instancia
#         instance.pk = existing_teacher.pk
#         instance.save = existing_teacher.save

