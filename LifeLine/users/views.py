def landing(request):
    return render(request, "landing.html")

def dashboard(request):
    # Placeholder for dashboard, will be implemented later
    return render(request, "base.html")

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        context = {
            "username": username,
            "email": email,
        }

        has_error = False

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            has_error = True

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            has_error = True

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            has_error = True

        # If any error occurred, redisplay form with values
        if has_error:
            return render(request, "register.html", context)

        # Otherwise create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, f"Account created for {username}! You can now log in.")
        return redirect("login")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        context = {"username": username}  # preserve username if login fails

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html", context)

    return render(request, "login.html")

def logout_view(request):
    auth_logout(request)
    return redirect("landing")
