from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .models import Exercise
from django import forms

class Exerciseform(forms.ModelForm):
    class Meta:
        model=Exercise
        fields=["name",
                "description",
                "instruction",
                "youtube_id"]
        
class UploadExerciseView(FormView):
    template_name = "Doctor/Upload_Exercise.html"
    form_class = Exerciseform
    success_url = reverse_lazy("ddashboard")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)