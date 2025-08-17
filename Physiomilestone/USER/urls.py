from django.urls import path,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.login_view,name="login"),
    path("register/",views.register_view,name="register"),
    path('logout/', views.logoutview, name='logout'),
]
