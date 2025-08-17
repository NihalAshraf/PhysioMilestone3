from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUSer(AbstractUser):
    ROLE_CHOICES=(
        ('child','Child'),
        ('doctor','Doctor'),
    )
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='child')
    age=models.PositiveIntegerField(null=True,blank=True)
    parent_name=models.CharField(max_length=50,blank=True)
    contact_number=models.CharField(max_length=50,blank=True)
