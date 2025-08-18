from django.urls import path
from . import views

urlpatterns = [
    path("Dashboard/",views.DashboardView.as_view(),name="ddashboard"),
    path("AssignExercise/",views.AssignExerciseView.as_view(),name="assignex"),
    path("PatientDetails/",views.PatientDetailView.as_view(),name="pdetails"),
    path("Uploadexercise/",views.UploadExerciseView.as_view(),name="uploadexercise"),
    path("patients/",views.PatientView.as_view(),name="patients"),
]
