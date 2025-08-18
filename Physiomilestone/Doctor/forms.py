from django import forms
from .models import Exercise

class Exerciseform(forms.ModelForm):
    class Meta:
        model=Exercise
        fields=["name",
                "description",
                "instruction",
                "youtube_id"]