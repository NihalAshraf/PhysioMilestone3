from django.db import models

# Create your models here.
class Exercise(models.Model):
    name=models.CharField(max_length=100,null=False)
    description=models.TextField()
    instruction=models.TextField(blank=True,null=True)
    youtube_id=models.CharField(max_length=200,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name