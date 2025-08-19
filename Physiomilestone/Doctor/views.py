from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.contrib import messages

from USER.models import CustomUSer
from Doctor.models import Exercise, AssignExercise

class DashboardView(TemplateView):
    template_name = "Doctor/Dashborad.html"

from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from USER.models import CustomUSer
from Doctor.models import Exercise, AssignExercise


class AssignExerciseView(TemplateView):
    template_name = "Doctor/Assign_Exercise.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patients = CustomUSer.objects.filter(role="child")
        exercises = Exercise.objects.all()
        context["patients"] = patients
        context["exercises"] = exercises
        return context

    def post(self, request, *args, **kwargs):
        patient_id = request.POST.get("patient")
        exercise_id = request.POST.get("exercise")
        reps = request.POST.get("reps")
        sets = request.POST.get("sets")
        instruction = request.POST.get("instruction")

        if patient_id and exercise_id:
            try:
                patient = CustomUSer.objects.get(id=patient_id)
                exercise = Exercise.objects.get(id=exercise_id)

                # ✅ Ensure reps and sets are integers
                reps = int(reps) if reps else 1
                sets = int(sets) if sets else 1

                AssignExercise.objects.create(
                    Patient_name=patient,
                    Exercise=exercise,
                    reps=reps,
                    sets=sets,
                    instruction=instruction,
                )

                messages.success(
                    request,
                    f"✅ Exercise '{exercise.name}' has been assigned to {patient.first_name} {patient.last_name}."
                )
            except CustomUSer.DoesNotExist:
                messages.error(request, "❌ Selected patient does not exist.")
            except Exercise.DoesNotExist:
                messages.error(request, "❌ Selected exercise does not exist.")
        else:
            messages.error(request, "❌ Please select both a patient and an exercise.")

        # ✅ Redirect after POST to prevent duplicate form submissions
        return redirect("assignex")


class PatientDetailView(TemplateView):
    template_name = "Doctor/Patient_Detail.html"

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
    template_name = "Doctor/patients.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        children = CustomUSer.objects.filter(role="child")
        context["patients"] = children
        return context
