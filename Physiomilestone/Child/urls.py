from django.urls import path
from . import views
urlpatterns = [
    path("Dashboard/",views.DashboardView.as_view(),name="cdashboard"),
    path("instruction/",views.ExerciseView.as_view(),name="instruction"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("progress/",views.progressView.as_view(),name="progress"),
    path("uploadexecise/",views.uploadexeciseView.as_view(),name="uploadexecise"),
]

