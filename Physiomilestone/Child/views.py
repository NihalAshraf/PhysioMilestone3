from django.shortcuts import render
from django.views.generic import TemplateView
from Doctor.models import AssignExercise

# Create your views here.
class DashboardView(TemplateView):
    template_name="Child/Dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["name"] =f"{user.first_name} {user.last_name}".strip()
        context["age"]=user.age
        context["parent"]=user.parent_name
        return context
        


class ExerciseView(TemplateView):
    template_name="child/Exercise_Instructions.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        assigned_exercise=AssignExercise.objects.filter(Patient_name=self.request.user).last()
        context["assigned_exercise"]=assigned_exercise
        return context

class ProfileView(TemplateView):
    template_name="child/Profile_Edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["name"] =f"{user.first_name} {user.last_name}" 
        return context
        

class progressView(TemplateView):
    template_name="child/Progress_Report_Detail.html"

class uploadexeciseView(TemplateView):
    template_name="child/Upload_Exercise.html"




