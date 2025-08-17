from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages

# Create your views here.
def register_view(request):
    if request=="POST":
        username="username"
        password="password"
        role=request.POST.get("role")

        user=user.objects.create(
            username
        )

def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            if user.role=="child":
                return redirect("child_dashboard")
            elif user.role=="doctor":
                return redirect("doctor_dashboard")
            else:
                message.error(request,"Invalid username or password")
    return render("USER/login.html")
        