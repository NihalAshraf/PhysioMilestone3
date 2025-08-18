from django.shortcuts import render
from django.views.generic import TemplateView
from USER.models import CustomUSer
from Doctor.models import Exercise
# Create your views here.
class DashboardView(TemplateView):
    template_name="Doctor/Dashborad.html"

class AssignExerciseView(TemplateView):
    template_name="Doctor/Assign_Exercise.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        patient=CustomUSer.objects.filter(role="child")
        exercises = Exercise.objects.all()
        context["patient"]=patient
        context["exercises"] = exercises
        return context



class PatientDetailView(TemplateView):
    template_name="Doctor/Patient_Detail.html"
    
class UploadExerciseView(TemplateView):
    template_name="Doctor/Upload_Exercise_Template.html"

class PatientView(TemplateView):
    template_name="Doctor/patients.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        children=CustomUSer.objects.filter(role="child")
        context["patients"]=children
        return context