from django.urls import path
from . import views

urlpatterns = [
    path("Dashboard/",views.DashboardView.as_view(),name="ddashboard"),
]
