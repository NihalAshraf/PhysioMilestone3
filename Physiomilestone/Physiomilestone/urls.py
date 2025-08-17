from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("USER.urls")),
    path("child/", include("Child.urls")),
    path("doctor/", include("Doctor.urls")),
]
