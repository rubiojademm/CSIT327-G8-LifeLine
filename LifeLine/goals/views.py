from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Goal

@login_required
def dashboard(request):
    user = request.user

    # Fetch user's goals
    user_goals = Goal.objects.filter(user=user)

    # Dynamic goal-based stats
    total_goals = user_goals.count()
    completed_goals = user_goals.filter(status="Completed").count()

    stats = {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "achievements": 15,     # STATIC — because achievements don't exist yet
        "streak": 7,            # STATIC — streak logic not implemented yet
    }

    # Recent goals pulled from DB
    recent_goals = user_goals.order_by('-created_at')[:5]

    # Static achievements (placeholder)
    recent_achievements = [
        {"id": 1, "title": "First Goal Completed", "date": "2 days ago"},
        {"id": 2, "title": "7-Day Streak", "date": "1 week ago"},
        {"id": 3, "title": "Goal Setter", "date": "2 weeks ago"},
    ]

    context = {
        "stats": stats,
        "recent_goals": recent_goals,
        "recent_achievements": recent_achievements,  # remains static
    }
    return render(request, "dashboard.html", context)


@login_required
def goals_page(request):
    user = request.user
    goals = Goal.objects.filter(user=user)

    # FILTERS
    search = request.GET.get("search", "")
    category = request.GET.get("category", "All")
    status = request.GET.get("status", "All")

    if search:
        goals = goals.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if category != "All":
        goals = goals.filter(category=category)

    if status != "All":
        goals = goals.filter(status=status)

    categories = ["All"] + list(goals.values_list("category", flat=True).distinct())
    statuses = ["All", "Not Started", "In Progress", "Completed"]

    context = {
        "goals": goals,
        "search": search,
        "category": category,
        "categories": categories,
        "status": status,
        "statuses": statuses,
    }
    return render(request, "goals_page.html", context)


@login_required
def create_goal(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        target_date = request.POST.get("target_date")

        Goal.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            target_date=target_date if target_date else None
        )
        return redirect("goals_page")

    return render(request, "create_goal.html")


@login_required
def update_progress(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)

    new_progress = min(goal.progress + 10, 100)
    goal.progress = new_progress
    goal.save()

    return redirect("goals_page")


@login_required
def delete_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    goal.delete()
    return redirect("goals_page")