from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
User = get_user_model()  # get your CustomUser model

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # create new user
        User.objects.create(
            username=username,
            password=make_password(password),  # hash password
            role=role
        )

        # after registration, redirect to login page
        return redirect("login")

    return render(request, "USER/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.role == "child":
                return redirect("cdashboard")   # goes to Child/Dashboard
            elif user.role == "doctor":
                return redirect("ddashboard")   # goes to Doctor/Dashboard
            else:
                messages.error(request, "Role not recognized!")
                return redirect("login")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "USER/login.html")


        