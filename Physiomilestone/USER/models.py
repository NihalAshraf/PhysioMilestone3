from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUSer(AbstractUser):
    ROLE_CHOICES=(
        ('child','Child'),
        ('doctor','Doctor'),
    )
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='child')