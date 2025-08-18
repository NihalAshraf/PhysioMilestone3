from django.shortcuts import render
from django.views.generic import TemplateView
from USER.models import CustomUSer
from Doctor.models import Exercise
from django.shortcuts import redirect
from django.views import View
from .models import Exercise
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
    


class UploadExerciseView(View):
    template_name = "Doctor/Upload_Exercise_Template.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        instruction = request.POST.get("instruction")
        youtube_id = request.POST.get("youtube_id")

        Exercise.objects.create(
            name=name,
            description=description,
            instruction=instruction,
            youtube_id=youtube_id
        )

        return redirect("ddashboard")


class PatientView(TemplateView):
    template_name="Doctor/patients.html"
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        children=CustomUSer.objects.filter(role="child")
        context["patients"]=children
        return context