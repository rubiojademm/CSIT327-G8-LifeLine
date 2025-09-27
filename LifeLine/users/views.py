from django.shortcuts import render, redirect

# Create your views here.
from .forms import RegisterForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("login")  # assuming you'll make login view next
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})
