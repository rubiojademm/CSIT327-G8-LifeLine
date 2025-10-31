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
from django.contrib.auth.decorators import login_required, user_passes_test
from supabase import create_client
from django.conf import settings
from django.db.models import Q


supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("admin_dashboard")

        # Handle actions
        if action == "delete":
            if request.user == user:
                messages.error(request, "You cannot delete your own account.")
            else:
                user.delete()
                messages.success(request, f"User '{user.username}' deleted successfully.")

        elif action == "deactivate":
            if not user.is_active:
                messages.info(request, f"User '{user.username}' is already inactive.")
            else:
                user.is_active = False
                user.save()
                messages.success(request, f"User '{user.username}' deactivated successfully.")

        elif action == "activate":
            if user.is_active:
                messages.info(request, f"User '{user.username}' is already active.")
            else:
                user.is_active = True
                user.save()
                messages.success(request, f"User '{user.username}' activated successfully.")

        return redirect("admin_dashboard")

    # Handle GET request (search and display users)
    query = request.GET.get("q", "").strip()
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).order_by("id")
    else:
        users = User.objects.all().order_by("id")

    user_count = users.count()

    return render(request, "admin_dashboard.html", {
        "users": users,
        "query": query,
        "user_count": user_count,
    })


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        # Keep user input so it persists when an error happens
        context = {
            "username": username,
            "email": email,
        }

        has_error = False

        # Validation checks
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            has_error = True

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            has_error = True

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            has_error = True

        # If there were any errors, reload the same page with messages
        if has_error:
            return render(request, "register.html", context)

        # Otherwise create the user and redirect
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, f"Account created for {username}! You can now log in.")
        return redirect("login")

    # GET request
    return render(request, "register.html")


def login_view(request):
    username = ""
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        context = {"username": username}  # preserve input on error

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            # Re-render the login page with username retained
            return render(request, "login.html", context)

    # When page first loads (GET)
    return render(request, "login.html", {"username": username})


def logout_view(request):
    auth_logout(request)
    return redirect("landing")


@login_required
def profile_view(request):
    user = request.user
    profile = getattr(user, "profile", None)

    if request.method == "POST":
        # Update user fields
        user.username = request.POST.get("username", user.username)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.save()

        # Update profile fields
        if profile:
            profile.bio = request.POST.get("bio", profile.bio)
            profile.location = request.POST.get("location", profile.location)
            profile.save()

        messages.success(request, "Your profile has been updated successfully.")
        return redirect("profile")

    # Placeholder stats & achievements
    stats = {
        "Goals Completed": "8",
        "Active Goals": "3",
        "Total Progress": "75%",
        "Streak Days": "12",
    }

    achievements = [
        "First Goal Completed",
        "Goal Achiever",
        "Weekly Streak",
        "Month Challenger",
    ]

    context = {
        "user": user,
        "profile": profile,
        "stats": stats,
        "achievements": achievements,
    }
    return render(request, "profile.html", context)