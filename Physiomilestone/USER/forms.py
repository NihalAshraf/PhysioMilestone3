from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUSer

class CustomusercreationForm(UserCreationForm):
    class Meta:
        model=CustomUSer
        fields=[
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'age',
            'parent_name',
            'contact_number',
            'role',
        ]