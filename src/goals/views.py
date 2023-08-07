import json
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Goals, GoalProgress
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views import View
from .forms import CreateGoalForm


class GoalCreateView(CreateView):
    model = Goals
    form_class = CreateGoalForm
    template_name = "goals/goal_definition.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_new_goal"] = True
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Add Teacher object to the form
        kwargs["teacher"] = self.request.user.user_teacher
        return kwargs

    def form_valid(self, form):
        # teacher is a field defined in the model Goals, techer field is excluded
        # from Form but we need this value for create a Goal
        form.instance.teacher = self.request.user.user_teacher
        # Setting the value of the course field which is mandaory field for create a Goal
        form.instance.course = self.request.user.user_teacher.course_set.first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home_teachers") + "?goal_created"


class GoalProgressView(ListView):
    model = GoalProgress
    template_name = "goals/goal_progress.html"

    def get_goal(self):
        goal_id = self.kwargs["goal_id"]
        goal = Goals.objects.get(id=goal_id)
        return goal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal = self.get_goal()
        context["goal_name"] = goal.name
        context["goal_course"] = goal.course
        context["goal_classroom"] = goal.classroom
        return context

    def get_queryset(self):
        goal = self.get_goal()
        goal_progress = GoalProgress.objects.filter(goals_id=goal.id)
        return goal_progress


class ProgressSaveView(View):
    def post(self, request, *args, **kwargs):
        jsonData = json.loads(request.body.decode("utf-8"))
        for prog_dic in jsonData:
            progress = prog_dic["progress"]
            comments = prog_dic["comments"]
            goal_id = prog_dic["goalId"]
            student_id = prog_dic["studentId"]
            obj, created = GoalProgress.objects.update_or_create(
                goals_id=goal_id,
                student_id=student_id,
                defaults={
                    "progress": progress,
                    "comments": comments,
                },
            )
        return JsonResponse({"result": "ok"})


class GoalUpdateView(UpdateView):
    model = Goals
    form_class = CreateGoalForm #Form reused from "GoalCreateView"
    template_name = "goals/goal_definition.html" # Template reused from "GoalCreateView"
    
    # This method is because we are reusing the form "CreateGoalForm" 
    # and this form expect the argument teacher in the __init__ method
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Add Teacher object to the form
        kwargs["teacher"] = self.request.user.user_teacher
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, "Objetivo actualizado exitosamente!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("home_teachers")
    

class GoalDeleteView(DeleteView):
    model = Goals

    def form_valid(self, form):
        record = self.get_object()
        record.delete()
        return JsonResponse({'result': 'goal_deleted'})