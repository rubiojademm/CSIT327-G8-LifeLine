# ==================== PROJECT STRUCTURE ====================
"""
lifeline_project/
│
├── lifeline_project/          # Main project folder
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                  # Authentication app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             # User Profile model
│   ├── forms.py              # Login/Register forms
│   ├── views.py              # Authentication views
│   ├── urls.py               # App URLs
│   └── templates/
│       └── accounts/
│           ├── landing.html  # Landing page
│           ├── login.html
│           └── register.html
│
├── core/                      # Main app (goals, achievements, etc.)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             # Goal, Achievement, Milestone models
│   ├── views.py              # Dashboard, profile, goals views
│   ├── urls.py
│   └── templates/
│       └── core/
│           ├── base.html     # Base template
│           ├── dashboard.html
│           ├── profile.html
│           ├── goals.html
│           └── achievements.html
│
├── static/                    # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                     # User uploads (profile pictures)
│
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
"""

# ==================== 1. settings.py (Main Configuration) ====================
"""
# lifeline_project/settings.py

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key-here-change-in-production'

DEBUG = True

ALLOWED_HOSTS = []

# ========== INSTALLED APPS ==========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your apps
    'accounts',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lifeline_project.urls'

# ========== TEMPLATES ==========
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lifeline_project.wsgi.application'

# ========== DATABASE ==========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ========== PASSWORD VALIDATION ==========
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ========== INTERNATIONALIZATION ==========
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ========== STATIC FILES ==========
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ========== MEDIA FILES ==========
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========== AUTH SETTINGS ==========
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:landing'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""


# ==================== 2. Main urls.py ====================
"""
# lifeline_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Landing, login, register
    path('app/', include('core.urls')),  # Dashboard, goals, etc.
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""


# ==================== 3. accounts/models.py ====================
"""
# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    # Link to Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile fields
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# ========== AUTO-CREATE PROFILE WHEN USER REGISTERS ==========
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""


# ==================== 4. accounts/forms.py ====================
"""
# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'you@example.com'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'John Doe'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes and placeholders
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm your password'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        # Use email as username
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'you@example.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password'
        })
    )
"""


# ==================== 5. accounts/views.py ====================
"""
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm

# ========== LANDING PAGE ==========
def landing_page(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'accounts/landing.html')


# ========== REGISTER VIEW ==========
def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in automatically after registration
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to LifeLine.')
            return redirect('core:dashboard')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


# ========== LOGIN VIEW ==========
def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('core:dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


# ========== LOGOUT VIEW ==========
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:landing')
"""


# ==================== 6. accounts/urls.py ====================
"""
# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
"""


# ==================== 7. core/models.py ====================
"""
# core/models.py

from django.db import models
from django.contrib.auth.models import User

# ========== GOAL MODEL ==========
class Goal(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress = models.IntegerField(default=0)  # 0-100
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    target_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


# ========== ACHIEVEMENT MODEL ==========
class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField()
    badge_icon = models.CharField(max_length=50, default='🏆')  # Emoji or image path
    earned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-earned_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


# ========== MILESTONE MODEL ==========
class Milestone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='milestones')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
"""


# ==================== 8. core/views.py ====================
"""
# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goal, Achievement, Milestone

# ========== DASHBOARD VIEW ==========
@login_required
def dashboard_view(request):
    user = request.user
    
    # Get user stats
    total_goals = Goal.objects.filter(user=user).count()
    completed_goals = Goal.objects.filter(user=user, status='completed').count()
    in_progress_goals = Goal.objects.filter(user=user, status='in_progress').count()
    total_achievements = Achievement.objects.filter(user=user).count()
    
    # Calculate progress percentage
    if total_goals > 0:
        progress_percentage = (completed_goals / total_goals) * 100
    else:
        progress_percentage = 0
    
    # Get recent achievements
    recent_achievements = Achievement.objects.filter(user=user)[:3]
    
    # Get active goals
    active_goals = Goal.objects.filter(user=user).exclude(status='completed')[:5]
    
    context = {
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'in_progress_goals': in_progress_goals,
        'total_achievements': total_achievements,
        'progress_percentage': round(progress_percentage, 1),
        'recent_achievements': recent_achievements,
        'active_goals': active_goals,
    }
    
    return render(request, 'core/dashboard.html', context)


# ========== PROFILE VIEW ==========
@login_required
def profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        # Handle profile updates
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        
        user.first_name = first_name
        user.email = email
        user.save()
        
        user.profile.bio = bio
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile.profile_picture = request.FILES['profile_picture']
        
        user.profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('core:profile')
    
    return render(request, 'core/profile.html', {'user': user})


# ========== GOALS VIEW ==========
@login_required
def goals_view(request):
    goals = Goal.objects.filter(user=request.user)
    return render(request, 'core/goals.html', {'goals': goals})


# ========== ACHIEVEMENTS VIEW ==========
@login_required
def achievements_view(request):
    achievements = Achievement.objects.filter(user=request.user)
    milestones = Milestone.objects.filter(user=request.user)
    
    context = {
        'achievements': achievements,
        'milestones': milestones,
    }
    
    return render(request, 'core/achievements.html', context)
"""


# ==================== 9. core/urls.py ====================
"""
# core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('goals/', views.goals_view, name='goals'),
    path('achievements/', views.achievements_view, name='achievements'),
]
"""


# ==================== 10. requirements.txt ====================
"""
Django>=4.2
Pillow>=10.0.0
"""


# ==================== SETUP INSTRUCTIONS ====================
"""
SETUP INSTRUCTIONS:

1. Create a virtual environment:
   python -m venv venv
   
2. Activate virtual environment:
   - Windows: venv\\Scripts\\activate
   - Mac/Linux: source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create Django project:
   django-admin startproject lifeline_project .

5. Create apps:
   python manage.py startapp accounts
   python manage.py startapp core

6. Copy the code from above into respective files

7. Run migrations:
   python manage.py makemigrations
   python manage.py migrate

8. Create superuser:
   python manage.py createsuperuser

9. Run the server:
   python manage.py runserver

10. Access the site:
    - Landing page: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/
"""
