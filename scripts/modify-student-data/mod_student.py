import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base.py")
django.setup()

from students.models import Student

with open('student_data.txt', 'r') as file:
    for line in file:
        line = line.split('\t')
        email = line[1].strip()
        rut = line[0].strip()
        student = Student.objects.get(email=email)
        student.name = student.name.title()
        student.rut = rut
        student.save()
        