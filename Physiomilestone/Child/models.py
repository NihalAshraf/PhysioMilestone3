from django.db import models
from Doctor.models import AssignExercise
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class ExerciseVideo(models.Model):
    assignment=models.ForeignKey(AssignExercise,on_delete=models.CASCADE,related_name="videos")
    video=models.FileField(upload_to="exercise_video/")
    uploaded_at=models.DateTimeField(auto_now_add=True)
    detected_exercise=models.CharField(max_length=100,blank=True,null=True)
    detected_reps=models.IntegerField(default=0)
    detected_sets=models.IntegerField(default=0)
    accuracy_score=models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    feedback=models.TextField(blank=True,null=True)
    
    # Additional fields for exercise validation
    exercise_type = models.CharField(max_length=50, blank=True, null=True)
    total_reps = models.IntegerField(default=0)
    total_sets = models.IntegerField(default=0)
    processing_status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ])
    processing_error = models.TextField(blank=True, null=True)
    frames_processed = models.IntegerField(default=0)
    
    # Validation results
    target_reps = models.IntegerField(default=0)
    target_sets = models.IntegerField(default=0)
    reps_accuracy = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    sets_accuracy = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    overall_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    def __str__(self):
        return f"Video for {self.assignment.Patient_name.first_name} - {self.assignment.Exercise.name}"
    
    def calculate_accuracy(self):
        """Calculate accuracy scores based on target vs detected values."""
        if self.target_reps > 0:
            self.reps_accuracy = min(100.0, (self.total_reps / self.target_reps) * 100)
        else:
            self.reps_accuracy = 0.0
            
        if self.target_sets > 0:
            self.sets_accuracy = min(100.0, (self.total_sets / self.target_sets) * 100)
        else:
            self.sets_accuracy = 0.0
            
        # Overall score is average of reps accuracy, sets accuracy, and pose accuracy
        self.overall_score = (self.reps_accuracy + self.sets_accuracy + self.accuracy_score) / 3
        self.save()

class ExerciseSession(models.Model):
    """Model to track exercise sessions and progress over time."""
    patient = models.ForeignKey('USER.CustomUSer', on_delete=models.CASCADE, related_name='exercise_sessions')
    assignment = models.ForeignKey(AssignExercise, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateTimeField(auto_now_add=True)
    total_duration = models.IntegerField(default=0)  # in seconds
    videos_uploaded = models.IntegerField(default=0)
    average_accuracy = models.FloatField(default=0.0)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Session for {self.patient.first_name} - {self.session_date.date()}"
