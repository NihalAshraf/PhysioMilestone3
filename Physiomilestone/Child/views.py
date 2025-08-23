from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.utils import timezone
from Doctor.models import AssignExercise, Consultation
from USER.models import CustomUSer
from .models import ExerciseVideo, ExerciseSession
from .utils.exercise_validator import ExerciseValidator
import os
import json
import logging
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

# Create your views here.
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name="Child/Dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["name"] =f"{user.first_name} {user.last_name}".strip()
        context["age"]=user.age
        context["parent"]=user.parent_name
        
        # Get recent exercise videos
        recent_videos = ExerciseVideo.objects.filter(
            assignment__Patient_name=user
        ).order_by('-uploaded_at')[:5]
        context["recent_videos"] = recent_videos
        
        # Get current assigned exercise
        current_exercise = AssignExercise.objects.filter(
            Patient_name=user
        ).last()
        context["current_exercise"] = current_exercise
        
        # Get pending consultations
        pending_consultations = Consultation.objects.filter(
            child=user,
            status='pending'
        ).count()
        context["pending_consultations"] = pending_consultations
        
        # Get recent consultations
        recent_consultations = Consultation.objects.filter(
            child=user
        ).order_by('-requested_at')[:3]
        context["recent_consultations"] = recent_consultations
        
        return context

@method_decorator(login_required, name='dispatch')
class ExerciseView(TemplateView):
    template_name="Child/Exercise_Instructions.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        assigned_exercise=AssignExercise.objects.filter(Patient_name=self.request.user).last()
        context["assigned_exercise"]=assigned_exercise
        return context

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name="Child/Profile_Edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["name"] =f"{user.first_name} {user.last_name}" 
        return context

@method_decorator(login_required, name='dispatch')
class progressView(TemplateView):
    template_name="Child/Progress_Report_Detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get exercise sessions and videos for progress tracking
        sessions = ExerciseSession.objects.filter(patient=user).order_by('-session_date')
        videos = ExerciseVideo.objects.filter(assignment__Patient_name=user).order_by('-uploaded_at')
        
        context["sessions"] = sessions
        context["videos"] = videos
        
        # Calculate overall progress
        if videos.exists():
            avg_accuracy = sum(v.overall_score for v in videos) / videos.count()
            context["overall_accuracy"] = round(avg_accuracy, 2)
        else:
            context["overall_accuracy"] = 0
        
        # Get recent videos for performance trends
        recent_videos = videos[:10]  # Last 10 videos
        
        # Prepare data for performance trends chart
        exercise_names = []
        accuracy_scores = []
        reps_completed = []
        dates = []
        
        for video in recent_videos:
            exercise_names.append(video.assignment.Exercise.name)
            accuracy_scores.append(video.overall_score)
            reps_completed.append(video.total_reps)
            dates.append(video.uploaded_at.strftime('%Y-%m-%d'))
        
        context["chart_data"] = {
            "exercise_names": exercise_names,
            "accuracy_scores": accuracy_scores,
            "reps_completed": reps_completed,
            "dates": dates
        }
        
        # Calculate exercise type breakdown for pie chart
        exercise_types = {}
        for video in videos:
            exercise_name = video.assignment.Exercise.name
            if exercise_name not in exercise_types:
                exercise_types[exercise_name] = {
                    'count': 0,
                    'total_accuracy': 0,
                    'total_reps': 0
                }
            exercise_types[exercise_name]['count'] += 1
            exercise_types[exercise_name]['total_accuracy'] += video.overall_score
            exercise_types[exercise_name]['total_reps'] += video.total_reps
        
        # Calculate averages and prepare pie chart data
        pie_chart_labels = []
        pie_chart_data = []
        pie_chart_colors = [
            'rgba(245, 158, 11, 0.8)',   # Amber
            'rgba(59, 130, 246, 0.8)',   # Blue
            'rgba(16, 185, 129, 0.8)',   # Green
            'rgba(239, 68, 68, 0.8)',    # Red
            'rgba(139, 92, 246, 0.8)',   # Purple
            'rgba(251, 146, 60, 0.8)',   # Orange
        ]
        
        for i, (exercise_name, stats) in enumerate(exercise_types.items()):
            pie_chart_labels.append(exercise_name)
            pie_chart_data.append(stats['count'])
            stats['avg_accuracy'] = round(stats['total_accuracy'] / stats['count'], 2)
        
        context["pie_chart_data"] = {
            "labels": pie_chart_labels,
            "data": pie_chart_data,
            "colors": pie_chart_colors[:len(pie_chart_labels)]
        }
        
        # Get weekly progress data for line chart
        from datetime import datetime, timedelta
        import calendar
        
        # Get last 4 weeks of data
        weekly_data = []
        weekly_labels = []
        
        for i in range(4):
            week_start = datetime.now().date() - timedelta(weeks=i+1)
            week_end = week_start + timedelta(days=6)
            
            week_videos = videos.filter(
                uploaded_at__date__gte=week_start,
                uploaded_at__date__lte=week_end
            )
            
            if week_videos.exists():
                week_avg_accuracy = sum(v.overall_score for v in week_videos) / week_videos.count()
                weekly_data.append(round(week_avg_accuracy, 2))
            else:
                weekly_data.append(0)
            
            weekly_labels.append(f"Week {4-i}")
        
        # Reverse to show chronological order
        weekly_data.reverse()
        weekly_labels.reverse()
        
        context["weekly_data"] = {
            "labels": weekly_labels,
            "data": weekly_data
        }
        
        # Calculate performance metrics
        if videos.exists():
            total_reps = sum(v.total_reps for v in videos)
            total_sets = sum(v.total_sets for v in videos)
            best_exercise = max(exercise_types.items(), key=lambda x: x[1]['avg_accuracy'])
            weakest_exercise = min(exercise_types.items(), key=lambda x: x[1]['avg_accuracy'])
            
            context["performance_metrics"] = {
                "total_reps": total_reps,
                "total_sets": total_sets,
                "total_sessions": sessions.count(),
                "best_exercise": best_exercise[0],
                "best_score": best_exercise[1]['avg_accuracy'],
                "weakest_exercise": weakest_exercise[0],
                "weakest_score": weakest_exercise[1]['avg_accuracy']
            }
        else:
            context["performance_metrics"] = {
                "total_reps": 0,
                "total_sets": 0,
                "total_sessions": 0,
                "best_exercise": "None",
                "best_score": 0,
                "weakest_exercise": "None",
                "weakest_score": 0
            }
        
        # Get assigned doctor information
        current_assignment = AssignExercise.objects.filter(Patient_name=user).last()
        if current_assignment:
            context["assigned_doctor"] = "Dr. " + current_assignment.Exercise.name  # Placeholder
        else:
            context["assigned_doctor"] = "Not assigned"
        
        return context

@method_decorator(login_required, name='dispatch')
class uploadexeciseView(TemplateView):
    template_name="Child/Upload_Exercise.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        assigned_exercise = AssignExercise.objects.filter(Patient_name=user).last()
        context["assigned_exercise"] = assigned_exercise
        return context

# New Consultation Views
@method_decorator(login_required, name='dispatch')
class DoctorListView(ListView):
    template_name = "Child/Doctor_List.html"
    context_object_name = "doctors"
    paginate_by = 10
    
    def get_queryset(self):
        return CustomUSer.objects.filter(role="doctor").order_by('first_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_doctors"] = self.get_queryset().count()
        return context

@method_decorator(login_required, name='dispatch')
class ConsultationRequestView(View):
    template_name = "Child/Consultation_Request.html"
    
    def get(self, request, doctor_id):
        doctor = get_object_or_404(CustomUSer, id=doctor_id, role="doctor")
        return render(request, self.template_name, {"doctor": doctor})
    
    def post(self, request, doctor_id):
        doctor = get_object_or_404(CustomUSer, id=doctor_id, role="doctor")
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if subject and message:
            Consultation.objects.create(
                child=request.user,
                doctor=doctor,
                subject=subject,
                message=message
            )
            messages.success(request, "Consultation request sent successfully!")
            return redirect('consultation_list')
        else:
            messages.error(request, "Please fill in all fields.")
            return render(request, self.template_name, {"doctor": doctor})

@method_decorator(login_required, name='dispatch')
class ConsultationListView(ListView):
    template_name = "Child/Consultation_List.html"
    context_object_name = "consultations"
    paginate_by = 10
    
    def get_queryset(self):
        return Consultation.objects.filter(child=self.request.user).order_by('-requested_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get counts by status
        context["pending_count"] = Consultation.objects.filter(
            child=user, status='pending'
        ).count()
        context["accepted_count"] = Consultation.objects.filter(
            child=user, status='accepted'
        ).count()
        context["completed_count"] = Consultation.objects.filter(
            child=user, status='completed'
        ).count()
        
        return context

@method_decorator(login_required, name='dispatch')
class ConsultationDetailView(DetailView):
    template_name = "Child/Consultation_Detail.html"
    model = Consultation
    context_object_name = "consultation"
    
    def get_queryset(self):
        return Consultation.objects.filter(child=self.request.user)

@method_decorator(login_required, name='dispatch')
class TestUploadView(View):
    """Simple test view to verify upload endpoint is working."""
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'success': True,
            'message': 'Upload endpoint is accessible',
            'user': request.user.username,
            'has_assigned_exercise': AssignExercise.objects.filter(Patient_name=request.user).exists()
        })

@method_decorator(login_required, name='dispatch')
class VideoUploadView(View):
    """Handle video upload and exercise validation."""
    
    def post(self, request, *args, **kwargs):
        try:
            # Get the uploaded video file
            video_file = request.FILES.get('video')
            if not video_file:
                logger.error("No video file provided in request")
                return JsonResponse({
                    'success': False,
                    'error': 'No video file provided'
                })
            
            # Log file information for debugging
            logger.info(f"Video file received: {video_file.name}, size: {video_file.size}, type: {video_file.content_type}")
            
            # Validate file type
            allowed_types = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv']
            if video_file.content_type not in allowed_types:
                logger.error(f"Invalid file type: {video_file.content_type}")
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid file type. Please upload MP4, AVI, MOV, or WMV files.'
                })
            
            # Validate file size (100MB limit)
            if video_file.size > 100 * 1024 * 1024:  # 100MB in bytes
                logger.error(f"File too large: {video_file.size} bytes")
                return JsonResponse({
                    'success': False,
                    'error': 'File size too large. Please upload a video smaller than 100MB.'
                })
            
            # Get current assigned exercise
            assigned_exercise = AssignExercise.objects.filter(
                Patient_name=request.user
            ).last()
            
            if not assigned_exercise:
                logger.error(f"No exercise assigned for user: {request.user.id}")
                return JsonResponse({
                    'success': False,
                    'error': 'No exercise assigned. Please contact your doctor.'
                })
            
            # Create ExerciseVideo instance
            exercise_video = ExerciseVideo.objects.create(
                assignment=assigned_exercise,
                video=video_file,
                target_reps=assigned_exercise.reps,
                target_sets=assigned_exercise.sets,
                processing_status='processing'
            )
            
            logger.info(f"ExerciseVideo created with ID: {exercise_video.id}")
            
            # Start processing in background (you might want to use Celery for this)
            self.process_video_async(exercise_video)
            
            return JsonResponse({
                'success': True,
                'video_id': exercise_video.id,
                'message': 'Video uploaded successfully. Processing...'
            })
            
        except Exception as e:
            logger.error(f"Error uploading video: {e}", exc_info=True)
            return JsonResponse({
                'success': False,
                'error': f'An error occurred while uploading the video: {str(e)}'
            })
    
    def process_video_async(self, exercise_video):
        """Process video asynchronously for exercise validation."""
        try:
            # Update status to processing
            exercise_video.processing_status = 'processing'
            exercise_video.save()
            
            # Initialize exercise validator
            validator = ExerciseValidator()
            
            # Get exercise type from assignment
            exercise_type = validator.get_exercise_type_from_name(
                exercise_video.assignment.Exercise.name
            )
            
            # Process the video
            video_path = exercise_video.video.path
            results = validator.process_video(video_path, exercise_type)
            
            if results.get('success', False):
                # Update video with results
                exercise_video.exercise_type = exercise_type
                exercise_video.detected_exercise = exercise_video.assignment.Exercise.name
                exercise_video.total_reps = results.get('total_reps', 0)
                exercise_video.total_sets = results.get('sets', 0)
                exercise_video.accuracy_score = results.get('accuracy', 0.0)
                exercise_video.frames_processed = results.get('frames_processed', 0)
                exercise_video.processing_status = 'completed'
                
                # Calculate accuracy scores
                exercise_video.calculate_accuracy()
                
                # Create or update exercise session
                session, created = ExerciseSession.objects.get_or_create(
                    patient=exercise_video.assignment.Patient_name,
                    assignment=exercise_video.assignment,
                    session_date__date=exercise_video.uploaded_at.date()
                )
                
                if not created:
                    session.videos_uploaded += 1
                
                # Calculate average accuracy for session
                session_videos = ExerciseVideo.objects.filter(
                    assignment__Patient_name=exercise_video.assignment.Patient_name,
                    uploaded_at__date=exercise_video.uploaded_at.date()
                )
                if session_videos.exists():
                    session.average_accuracy = sum(v.overall_score for v in session_videos) / session_videos.count()
                
                session.save()
                
            else:
                exercise_video.processing_status = 'failed'
                exercise_video.processing_error = results.get('error', 'Unknown error')
                exercise_video.save()
                
        except Exception as e:
            logger.error(f"Error processing video {exercise_video.id}: {e}")
            exercise_video.processing_status = 'failed'
            exercise_video.processing_error = str(e)
            exercise_video.save()

@method_decorator(login_required, name='dispatch')
class VideoStatusView(View):
    """Check video processing status."""
    
    def get(self, request, video_id):
        try:
            video = get_object_or_404(ExerciseVideo, id=video_id, assignment__Patient_name=request.user)
            
            return JsonResponse({
                'success': True,
                'status': video.processing_status,
                'results': {
                    'exercise_type': video.exercise_type,
                    'total_reps': video.total_reps,
                    'total_sets': video.total_sets,
                    'accuracy_score': video.accuracy_score,
                    'overall_score': video.overall_score,
                    'reps_accuracy': video.reps_accuracy,
                    'sets_accuracy': video.sets_accuracy,
                    'target_reps': video.target_reps,
                    'target_sets': video.target_sets,
                } if video.processing_status == 'completed' else None,
                'error': video.processing_error if video.processing_status == 'failed' else None
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'Error retrieving video status'
            })

@method_decorator(login_required, name='dispatch')
class ExerciseResultsView(TemplateView):
    """Display exercise results after processing."""
    template_name = "Child/Exercise_Results.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_id = self.kwargs.get('video_id')
        video = get_object_or_404(ExerciseVideo, id=video_id, assignment__Patient_name=self.request.user)
        
        context['video'] = video
        context['assignment'] = video.assignment
        
        return context



