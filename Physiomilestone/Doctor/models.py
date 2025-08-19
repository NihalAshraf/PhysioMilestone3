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

    def __str__(self):
        return f"{self.Exercise.name} for {self.Patient_name.first_name}"
