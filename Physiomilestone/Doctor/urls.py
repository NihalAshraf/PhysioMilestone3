from django.urls import path
from . import views

urlpatterns = [
    path("Dashboard/",views.DashboardView.as_view(),name="ddashboard"),
    path("AssignExercise/",views.AssignExerciseView.as_view(),name="assignex"),
    path("patients/",views.PatientListView.as_view(),name="patient_list"),
    path("patient/<int:pk>/",views.PatientDetailView.as_view(),name="patient_detail"),
    path("patient/<int:pk>/progress/",views.PatientProgressView.as_view(),name="patient_progress"),
    path("consultations/",views.ConsultationListView.as_view(),name="consultation_list"),
    path("consultation/<int:pk>/",views.ConsultationDetailView.as_view(),name="consultation_detail"),
    path("consultation/<int:consultation_id>/respond/",views.ConsultationResponseView.as_view(),name="consultation_response"),
    path("Uploadexercise/",views.UploadExerciseView.as_view(),name="uploadexercise"),
    path("PatientDetails/",views.PatientDetailView.as_view(),name="pdetails"),  # Keep for backward compatibility
]
