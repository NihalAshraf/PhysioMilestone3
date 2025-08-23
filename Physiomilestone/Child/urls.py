from django.urls import path
from . import views
urlpatterns = [
    path("Dashboard/",views.DashboardView.as_view(),name="cdashboard"),
    path("instruction/",views.ExerciseView.as_view(),name="instruction"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("progress/",views.progressView.as_view(),name="progress"),
    path("uploadexecise/",views.uploadexeciseView.as_view(),name="uploadexecise"),
    
    # Video upload and processing endpoints
    path("upload-video/", views.VideoUploadView.as_view(), name="upload_video"),
    path("video-status/<int:video_id>/", views.VideoStatusView.as_view(), name="video_status"),
    path("exercise-results/<int:video_id>/", views.ExerciseResultsView.as_view(), name="exercise_results"),
]

