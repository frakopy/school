from email.policy import default
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from courses.models import Course
from students.models import Student
from teachers.models import Teacher

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html' 
    redirect_authenticated_user = True 

    def get_success_url(self):
        is_student = Student.objects.filter(user=self.request.user).exists()
        is_teacher = Teacher.objects.filter(user=self.request.user).exists()

        if is_student:
            return reverse_lazy('create_records_student')
        elif is_teacher:
            teacher = self.request.user.user_teacher
            courses = teacher.course_set.all()
            if courses:
                # If teacher has a course that means is not a head teacher
                return reverse_lazy('home_teachers')
            else:
                # If teacher has not a course is a head teacher
                return reverse_lazy('head_teachers')


class CustomLogoutView(LogoutView):
    next_page = 'login'
