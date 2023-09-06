import json
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from goals.models import GoalProgress, Goals
from students.models import Student
from courses.models import Course
from classrooms.models import Classroom, Level
from .models import Record
from datetime import datetime, timedelta
from django.contrib import messages
from .forms import EditRecordForm, StudentRecordUpdateForm
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin

class TotalRecordsView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    model = Record
    template_name = "records/records.html"

    def get_queryset(self):
        teacher = self.request.user.user_teacher
        classrooms = teacher.classroom_set.all()
        return Record.objects.filter(
            student__classroom__in=classrooms, course__teacher=teacher
        )


class RecordsView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    model = Record
    template_name = "records/records.html"

    def get_queryset(self):
        classroom_id = self.kwargs["classroom_id"]
        hour_str = self.kwargs["hour_str"]
        hour = datetime.strptime(hour_str, "%H:%M")

        now = datetime.now().strftime("%Y-%m-%d")
        now_formatted = datetime.strptime(now, "%Y-%m-%d").date()

        try:
            return Record.objects.filter(
                course__teacher=self.request.user.user_teacher,
                schedule__classroom_id=classroom_id,
                start_date=now_formatted,
                schedule__hour=hour,
            )
        except Exception as e:
            print(e)
            return Record.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user.user_teacher
        classroom_id = self.kwargs["classroom_id"]
        goals = list(
            Goals.objects.filter(teacher=teacher, classroom_id=classroom_id).values()
        )
        context["goals"] = json.dumps(goals)

        return context


class GetJsonProgressView(RecordsView, LoginRequiredMixin):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        progress_student = []
        records = self.get_queryset()
        for record in records:
            progress_student += list(
                GoalProgress.objects.filter(student_id=record.student_id).values(
                    "goals__name", "progress", "goals_id", "student_id", "comments"
                )
            )
        return JsonResponse({"json_progress": progress_student})


class SaveRecordsView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        classroom_id = self.kwargs["classroom_id"]
        hour = self.kwargs["hour_str"]
        self.data = request.POST.copy()
        self.csrf_token = self.data.pop("csrfmiddlewaretoken", None)
        self.record_objects = []
        for record in Record.objects.all():
            self.id = record.id
            self.input_name = f"id_{self.id}"
            self.comment_name = f"comment_id_{self.id}"
            if self.input_name in self.data:
                record.present = True
            else:
                record.present = False
            if self.comment_name in self.data:
                record.comments = self.data[self.comment_name]

            self.record_objects.append(record)

        try:
            Record.objects.bulk_update(self.record_objects, ["present", "comments"])
            messages.success(
                request, "Los registros se han guardado con éxito en la base de datos"
            )
            return redirect(reverse("records_list", args=[classroom_id, hour]))
        except Exception as e:
            print(e)
            messages.error(
                request, "Algo salió mal al momento de guardar los registros"
            )
            return redirect(reverse("records_list", args=[classroom_id, hour]))


class CreateRecordsStudentView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def filtered_records(self):
        student = self.request.user.student
        today_num_week = datetime.now().weekday()
        days_to_add = 7 - today_num_week
        next_monday = (datetime.now() + timedelta(days=days_to_add)).date()
        next_sunday = next_monday + timedelta(days=6)
        records = Record.objects.filter(
            start_date__gte=next_monday,
            start_date__lte=next_sunday,
            student=student,
        )
        return records

    def json_list(self):
        records = self.filtered_records()
        json_list = []
        for record in records:
            json_list.append(
                {
                    "hour": record.schedule.hour.strftime("%H:%M"),
                    "day": record.schedule.day,
                    "course": record.course.name,
                    "hour_block": record.schedule.hour_block,
                    "record_id": record.id,
                }
            )
        return json_list

    def get_next_date(self, day):
        weekdays = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        today_num_week = datetime.now().weekday()
        days_to_add = (7 - today_num_week) + weekdays.index(day)
        next_day = (datetime.now() + timedelta(days=days_to_add)).date()
        return next_day

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        student = self.request.user.student
        classroom = student.classroom
        if not classroom:
            base_url = f"http://{request.META['HTTP_HOST']}"
            return HttpResponse(
                f"""
                    <h2>
                        El alumno '{student}' aun no tiene un classroom asignado <br>
                        por favor solicite al Admin que le asigne un classroom
                    </h2>
                    <a href="{base_url}/authentication/logout">Salir</a>
                    """
            )
        schedules = classroom.classroom_schedule.all()
        schedule_list = list(schedules.values())
        teachers_in_classroom = classroom.teacher.all()
        courses = list(
            Course.objects.filter(teacher__in=teachers_in_classroom).values()
        )

        max_availability = classroom.level.availability
        for c in courses:
            num_records_in_db = len(Record.objects.filter(course_id=c['id']))
            current_availability = max_availability - num_records_in_db
            c['availability'] = current_availability
        
        data = {
            "student_id": student.id,
            "schedules": schedule_list,
            "courses": courses,
            "json_list": self.json_list(),
        }

        for schedule in data["schedules"]:
            schedule["hour"] = schedule["hour"].strftime("%H:%M")

        json_data = json.dumps(data, ensure_ascii=False)

        return render(request, "records/student_records.html", {"json_data": json_data})

    def checkAvailability(self, request, records_to_save):
        classroom = request.user.student.classroom
        availability = classroom.level.availability
        teachers_in_classroom = classroom.teacher.all()
        courses = Course.objects.filter(teacher__in=teachers_in_classroom)

        # Getting next monday and sunday
        today_num_week = datetime.now().weekday()
        days_to_add = (7 - today_num_week)
        next_monday = (datetime.now() + timedelta(days=days_to_add)).date()
        next_sunday = next_monday + timedelta(days=6)

        result = {"available": True}
        for c in courses:
            courses_filtered =  list(filter(lambda r: r["course"] == c.name, records_to_save))
            if courses_filtered:
                num_records_to_save = len(courses_filtered)
                q = Q(course=c) & Q(start_date__range=(next_monday, next_sunday))
                num_records_in_db = len(Record.objects.filter(q))

                if availability == num_records_in_db:
                    result["available"] = False
                    result["num_available"] = 0
                    result["course_name"] = c.name
                    result["num_records_sent"] = num_records_to_save
                elif availability < num_records_to_save + num_records_in_db:
                    num_available = availability - num_records_in_db
                    result["available"] = False
                    result["num_available"] = num_available
                    result["course_name"] = c.name
                    result["num_records_sent"] = num_records_to_save

        return result

    def post(self, request, *args, **kwargs):
        dictFromPost = json.loads(request.body.decode("utf-8"))
        records = dictFromPost["jsonData"]
        # Check if records list is empty
        if not records:
            return JsonResponse({"result": "empty_list"})
        
        # Check avaibility by course
        result = self.checkAvailability(request, records)
        if not result["available"]:
            return JsonResponse(
                {
                    "result": "no_availability",
                    "course_name": result["course_name"],
                    "num_available": result["num_available"],
                    "num_records_sent": result["num_records_sent"],
                }
            )

        record_list = []
        for record in records:
            # Get Studen object
            student_id = record.get("studentId", False)
            student = Student.objects.get(id=student_id)

            # Get Classroom object
            classroom_id = record.get("classroom_id", False)
            classroom = Classroom.objects.get(id=classroom_id)

            # Get Teacher object
            teachers = classroom.teacher.all()

            # Get Schedule object
            day = record.get("day", False)
            hour = record.get("hour", False)
            hour_obj = datetime.strptime(hour, "%H:%M")
            schedule = classroom.classroom_schedule.filter(
                day=day, hour=hour_obj
            ).first()

            # Get next day of the week
            start_date = self.get_next_date(day)

            # Get Course object
            course_name = record.get("course", False)

            course = Course.objects.filter(
                Q(name=course_name) & Q(teacher__in=teachers)
            ).first()

            # Creating a list of Record objects
            record_list.append(
                Record(
                    student=student,
                    schedule=schedule,
                    course=course,
                    start_date=start_date,
                )
            )
        try:
            # Create Records in the DB
            new_records = Record.objects.bulk_create(record_list)

            # Create a list of json with records information
            records_created = []
            for record in new_records:
                records_created.append({
                    "hour": record.schedule.hour.strftime("%H:%M"),
                    "day": record.schedule.day,
                    "course": record.course.name,
                    "hour_block": record.schedule.hour_block,
                    "record_id": record.id
                })

            json_data = json.dumps(records_created, ensure_ascii=False)
            return JsonResponse({"result": "ok", "records_created": json_data})

        except Exception as e:
            return JsonResponse({"result": str(e)})


class StudentScheduleWeekView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    model = Record
    template_name = "records/student_schedule_week.html"

    def get_queryset(self):
        student_id = self.kwargs["student_id"]
        today_num_week = datetime.now().weekday()
        this_monday = (datetime.now() - timedelta(days=today_num_week)).date()
        this_sunday = this_monday + timedelta(days=6)
        queryset = Record.objects.filter(
            student_id=student_id,
            start_date__gte=this_monday,
            start_date__lte=this_sunday,
        )
        return queryset


class UpdateRecordsView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')

    model = Record
    form_class = EditRecordForm
    template_name = "records/update_records.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_name"] = self.object.student
        return context

    def form_valid(self, form):
        messages.success(self.request, "Información actualizada con éxito!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("total_records")


class StudentRecordView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')

    model = Record
    template_name = "records/student_records_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs["student_id"]
        student = Student.objects.get(id=student_id)
        progress_set_student = student.student_progress.all()
        context["student_name"] = student.name
        context["progress_set_student"] = progress_set_student
        if student.classroom:
            context["student_classroom"] = student.classroom
        else:
            context["student_classroom"] = "Sin Classroom asignado"
        previous_url = self.request.GET.get("previous_url", "")
        context["previous_url"] = previous_url
        return context

    def get_queryset(self):
        student_id = self.kwargs["student_id"]
        teacher_id = self.kwargs["teacher_id"]
        return Record.objects.filter(
            student_id=student_id, course__teacher_id=teacher_id
        )


class StudentRecordUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')

    model = Record
    form_class = StudentRecordUpdateForm
    template_name = "records/student_record_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        previous_url = self.request.GET.get("previous_url", "")
        context['previous_url'] = previous_url
        return context

    def get_success_url(self):
        record = self.object
        student_id = record.student_id
        teacher_id = record.course.teacher_id
        studen_detail_url = self.request.GET.get("previous_url", "")
        return (
            reverse_lazy("student_records", args=[student_id, teacher_id])
            + "?updated"
            + "&previous_url="
            + studen_detail_url
        )


class StudentRecordDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')

    model = Record

    def form_valid(self, form):
        record = self.get_object()
        record.delete()
        return JsonResponse({"result": "record_deleted"})
