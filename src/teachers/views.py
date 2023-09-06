from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from classrooms.models import Classroom
from records.models import Record
import datetime


class ClassroomListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    model = Classroom
    template_name = "teachers/home_teachers.html"

    def get_classrooms(self):
        teacher = self.request.user.user_teacher
        print(datetime.datetime.now())
        return Classroom.objects.filter(teacher=teacher)

    def get_total_records(self):
        try:
            classrooms = self.get_classrooms()
            now = datetime.datetime.now().strftime("%Y-%m-%d")
            now_formatted = datetime.datetime.strptime(now, "%Y-%m-%d").date()
            block_hour_set = set(
                classrooms[0].classroom_schedule.all().values_list("hour", "hour_block")
            )

            class_dic = {}

            for classroom in classrooms:
                for b in block_hour_set:
                    hour = b[0]
                    block = b[1]
                    total_records = Record.objects.filter(
                        course__teacher=self.request.user.user_teacher,
                        schedule__classroom_id=classroom.id,
                        start_date=now_formatted,
                        schedule__hour=hour,
                    )
                    if classroom in class_dic:
                        class_dic[classroom][f"records_for_block{block}"] = len(
                            total_records
                        )
                        class_dic[classroom][f"hour_for_block{block}"] = hour.strftime('%H:%M')
                    else:
                        class_dic[classroom] = {
                            f"records_for_block{block}": len(total_records),
                            f"hour_for_block{block}": hour.strftime('%H:%M'),
                        }
            return class_dic
        except Exception as e:
            print(e)
            class_dic = {}
            return class_dic

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class_dic"] = self.get_total_records()
        return context

    def get_queryset(self):
        return self.get_classrooms()


class UncompletedScheduleView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    model = Record
    template_name = "teachers/head_teachers.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        today_num_week = datetime.datetime.now().weekday()
        monday = (
            datetime.datetime.now() - datetime.timedelta(days=today_num_week)
        ).date()
        sunday = monday + datetime.timedelta(days=6)
        pks_students_with_schedule = queryset.filter(
            start_date__gte=monday,
            start_date__lte=sunday,
        ).values_list("student", flat=True)

        teacher = self.request.user.user_teacher
        classroom = teacher.classroom_set.all().first()
        total_students = classroom.students.all()
        students_without_schedule = total_students.exclude(
            pk__in=[pk for pk in pks_students_with_schedule]
        )
        return students_without_schedule
