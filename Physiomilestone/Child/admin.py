from django.contrib import admin
from .models import ExerciseVideo, ExerciseSession

@admin.register(ExerciseVideo)
class ExerciseVideoAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'uploaded_at', 'exercise_type', 'total_reps', 'total_sets', 'overall_score', 'processing_status']
    list_filter = ['processing_status', 'exercise_type', 'uploaded_at']
    search_fields = ['assignment__Patient_name__first_name', 'assignment__Patient_name__last_name', 'assignment__Exercise__name']
    readonly_fields = ['uploaded_at', 'frames_processed']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('assignment', 'video', 'uploaded_at')
        }),
        ('Exercise Detection', {
            'fields': ('exercise_type', 'detected_exercise', 'processing_status', 'processing_error', 'frames_processed')
        }),
        ('Results', {
            'fields': ('total_reps', 'total_sets', 'accuracy_score', 'target_reps', 'target_sets')
        }),
        ('Accuracy Scores', {
            'fields': ('reps_accuracy', 'sets_accuracy', 'overall_score')
        }),
        ('Feedback', {
            'fields': ('feedback',)
        }),
    )

@admin.register(ExerciseSession)
class ExerciseSessionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'assignment', 'session_date', 'videos_uploaded', 'average_accuracy']
    list_filter = ['session_date', 'patient']
    search_fields = ['patient__first_name', 'patient__last_name', 'assignment__Exercise__name']
    readonly_fields = ['session_date']
