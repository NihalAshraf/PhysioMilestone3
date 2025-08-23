from django.db import models
from USER.models import CustomUSer

class Exercise(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()
    instruction = models.TextField(blank=True, null=True)
    youtube_id = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AssignExercise(models.Model):
    Patient_name = models.ForeignKey(CustomUSer, on_delete=models.CASCADE, related_name="assigned_exercises")
    Exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.IntegerField()
    sets = models.IntegerField()
    instruction = models.TextField(blank=True, null=True)
    assigned_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.Exercise.name} for {self.Patient_name.first_name}"

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    child = models.ForeignKey(CustomUSer, on_delete=models.CASCADE, related_name='consultations_requested')
    doctor = models.ForeignKey(CustomUSer, on_delete=models.CASCADE, related_name='consultations_received')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    doctor_response = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Consultation: {self.child.first_name} - {self.doctor.first_name}"

class PatientProgress(models.Model):
    """Model to track overall patient progress for doctor monitoring"""
    patient = models.ForeignKey(CustomUSer, on_delete=models.CASCADE, related_name='progress_records')
    doctor = models.ForeignKey(CustomUSer, on_delete=models.CASCADE, related_name='patient_progress')
    date = models.DateField(auto_now_add=True)
    total_exercises_completed = models.IntegerField(default=0)
    average_accuracy = models.FloatField(default=0.0)
    total_sessions = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['patient', 'doctor', 'date']
    
    def __str__(self):
        return f"Progress: {self.patient.first_name} - {self.date}"
