from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta

from USER.models import CustomUSer
from Doctor.models import Exercise, AssignExercise, Consultation, PatientProgress
from Child.models import ExerciseVideo, ExerciseSession

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = "Doctor/Dashborad.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.request.user
        
        # Get doctor's patients
        patients = CustomUSer.objects.filter(role="child")
        context["total_patients"] = patients.count()
        
        # Get pending consultations
        pending_consultations = Consultation.objects.filter(
            doctor=doctor, 
            status='pending'
        ).count()
        context["pending_consultations"] = pending_consultations
        
        # Get recent exercise assignments
        recent_assignments = AssignExercise.objects.filter(
            is_active=True
        ).order_by('-assigned_on')[:5]
        context["recent_assignments"] = recent_assignments
        
        # Get today's progress summary
        today = timezone.now().date()
        today_progress = PatientProgress.objects.filter(
            doctor=doctor,
            date=today
        ).count()
        context["today_progress"] = today_progress
        
        return context

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class PatientListView(ListView):
    template_name = "Doctor/Patient_List.html"
    context_object_name = "patients"
    paginate_by = 10
    
    def get_queryset(self):
        return CustomUSer.objects.filter(role="child").order_by('first_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_patients"] = self.get_queryset().count()
        return context

@method_decorator(login_required, name='dispatch')
class PatientDetailView(DetailView):
    template_name = "Doctor/Patient_Detail.html"
    model = CustomUSer
    context_object_name = "patient"
    
    def get_queryset(self):
        return CustomUSer.objects.filter(role="child")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object
        
        # Get patient's exercise assignments
        assignments = AssignExercise.objects.filter(Patient_name=patient).order_by('-assigned_on')
        context["assignments"] = assignments
        
        # Get patient's exercise videos
        videos = ExerciseVideo.objects.filter(assignment__Patient_name=patient).order_by('-uploaded_at')
        context["videos"] = videos
        
        # Get patient's exercise sessions
        sessions = ExerciseSession.objects.filter(patient=patient).order_by('-session_date')
        context["sessions"] = sessions
        
        # Calculate overall progress
        if videos.exists():
            avg_accuracy = sum(v.overall_score for v in videos) / videos.count()
            context["overall_accuracy"] = round(avg_accuracy, 2)
            context["total_exercises"] = videos.count()
        else:
            context["overall_accuracy"] = 0
            context["total_exercises"] = 0
        
        # Get recent progress (last 7 days)
        week_ago = timezone.now().date() - timedelta(days=7)
        recent_videos = videos.filter(uploaded_at__date__gte=week_ago)
        context["recent_videos"] = recent_videos
        
        # Get pending exercises
        pending_assignments = assignments.filter(is_active=True, completed=False)
        context["pending_assignments"] = pending_assignments
        
        return context

@method_decorator(login_required, name='dispatch')
class PatientProgressView(DetailView):
    template_name = "Doctor/Patient_Progress.html"
    model = CustomUSer
    context_object_name = "patient"
    
    def get_queryset(self):
        return CustomUSer.objects.filter(role="child")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object
        
        # Get progress over time (last 30 days)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        videos = ExerciseVideo.objects.filter(
            assignment__Patient_name=patient,
            uploaded_at__date__gte=thirty_days_ago
        ).order_by('uploaded_at')
        
        # Prepare data for charts
        dates = []
        accuracies = []
        reps_completed = []
        
        for video in videos:
            dates.append(video.uploaded_at.strftime('%Y-%m-%d'))
            accuracies.append(video.overall_score)
            reps_completed.append(video.total_reps)
        
        # Calculate totals
        total_reps = sum(reps_completed) if reps_completed else 0
        total_accuracy = sum(accuracies) if accuracies else 0
        avg_accuracy = total_accuracy / len(accuracies) if accuracies else 0
        
        context["chart_data"] = {
            "dates": dates,
            "accuracies": accuracies,
            "reps_completed": reps_completed,
            "total_reps": total_reps,
            "total_accuracy": total_accuracy,
            "avg_accuracy": round(avg_accuracy, 2)
        }
        
        # Get exercise type breakdown
        exercise_types = {}
        for video in videos:
            exercise_name = video.assignment.Exercise.name
            if exercise_name not in exercise_types:
                exercise_types[exercise_name] = {
                    'count': 0,
                    'avg_accuracy': 0,
                    'total_reps': 0
                }
            exercise_types[exercise_name]['count'] += 1
            exercise_types[exercise_name]['avg_accuracy'] += video.overall_score
            exercise_types[exercise_name]['total_reps'] += video.total_reps
        
        # Calculate averages
        for exercise_type in exercise_types.values():
            if exercise_type['count'] > 0:
                exercise_type['avg_accuracy'] = round(exercise_type['avg_accuracy'] / exercise_type['count'], 2)
        
        context["exercise_types"] = exercise_types
        
        return context

@method_decorator(login_required, name='dispatch')
class ConsultationListView(ListView):
    template_name = "Doctor/Consultation_List.html"
    context_object_name = "consultations"
    paginate_by = 10
    
    def get_queryset(self):
        doctor = self.request.user
        return Consultation.objects.filter(doctor=doctor).order_by('-requested_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.request.user
        
        # Get counts by status
        context["pending_count"] = Consultation.objects.filter(
            doctor=doctor, status='pending'
        ).count()
        context["accepted_count"] = Consultation.objects.filter(
            doctor=doctor, status='accepted'
        ).count()
        context["completed_count"] = Consultation.objects.filter(
            doctor=doctor, status='completed'
        ).count()
        
        return context

@method_decorator(login_required, name='dispatch')
class ConsultationDetailView(DetailView):
    template_name = "Doctor/Consultation_Detail.html"
    model = Consultation
    context_object_name = "consultation"
    
    def get_queryset(self):
        doctor = self.request.user
        return Consultation.objects.filter(doctor=doctor)

@method_decorator(login_required, name='dispatch')
class ConsultationResponseView(View):
    def post(self, request, consultation_id):
        consultation = get_object_or_404(Consultation, id=consultation_id, doctor=request.user)
        response = request.POST.get('response')
        action = request.POST.get('action')
        
        if action == 'accept':
            consultation.status = 'accepted'
            consultation.accepted_at = timezone.now()
            messages.success(request, "Consultation accepted successfully.")
        elif action == 'complete':
            consultation.status = 'completed'
            consultation.completed_at = timezone.now()
            messages.success(request, "Consultation marked as completed.")
        elif action == 'respond':
            if response:
                consultation.doctor_response = response
                consultation.status = 'accepted'
                consultation.accepted_at = timezone.now()
                messages.success(request, "Response sent successfully.")
            else:
                messages.error(request, "Please provide a response.")
        
        consultation.save()
        return redirect('consultation_detail', pk=consultation_id)

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

@method_decorator(login_required, name='dispatch')
class PatientView(TemplateView):
    template_name = "Doctor/patients.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        children = CustomUSer.objects.filter(role="child")
        context["patients"] = children
        return context
