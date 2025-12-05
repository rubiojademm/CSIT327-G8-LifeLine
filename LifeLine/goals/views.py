from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Goal, GoalProgressLog
from .models import Milestone, UserMilestone


# DASHBOARD PAGE #
@login_required
def dashboard(request):
    user_goals = Goal.objects.filter(user=request.user)

    total_goals = user_goals.count()
    completed_goals = user_goals.filter(status="Completed").count()
    in_progress_goals = user_goals.filter(status="In Progress").count()
    not_started_goals = user_goals.filter(status="Not Started").count()

    # Compute completion rate safely
    completion_rate = (completed_goals / total_goals) * 100 if total_goals > 0 else 0

    # Get recent goals (latest 3)
    recent_goals = user_goals.order_by('-created_at')[:3]

    stats = {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "in_progress_goals": in_progress_goals,
        "not_started_goals": not_started_goals,
        "streak": 0,  # You can calculate a streak later if needed
        "completion_rate": round(completion_rate),
    }

    context = {
        "stats": stats,
        "recent_goals": recent_goals,
    }
    return render(request, "dashboard.html", context)


# GOALS PAGE #
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

    if request.method == "POST":
        new_progress = int(request.POST.get("progress", goal.progress))

        # Clamp between 0 and 100
        goal.progress = max(0, min(100, new_progress))
        goal.save()

    return redirect("goals_page")


@login_required
def delete_goal(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    goal.delete()
    return redirect("goals_page")


# ACHIEVEMENT PAGE #
@login_required
def milestones_page(request):
    milestones = Milestone.objects.all()
    user_milestones = UserMilestone.objects.filter(
        user=request.user,
        milestone__in=milestones
    )

    milestone_map = {
        um.milestone_id: um for um in user_milestones
    }

    final_data = []
    for m in milestones:
        user_m = milestone_map.get(m.id)
        final_data.append({
            "milestone": m,
            "unlocked": user_m.unlocked if user_m else False,
            "date": user_m.unlocked_at if user_m else None
        })

    return render(request, "milestones.html", {
        "milestones": final_data
    })


# REPORTS PAGE #
@login_required
def reports_page(request):
    return render(request, "reports.html")


# TIMELINE CHART
@login_required
def report_timeline(request):
    goals = Goal.objects.filter(user=request.user).order_by("created_at")

    data = {
        "labels": [g.created_at.strftime("%Y-%m-%d") for g in goals],
        "values": list(range(1, goals.count() + 1)),
    }

    return JsonResponse(data)


# STATUS DISTRIBUTION
@login_required
def report_status(request):
    data = (
        Goal.objects.filter(user=request.user)
        .values("status")
        .annotate(total=Count("status"))
    )

    return JsonResponse(list(data), safe=False)


# CATEGORY DISTRIBUTION
@login_required
def report_categories(request):
    data = (
        Goal.objects.filter(user=request.user)
        .values("category")
        .annotate(total=Count("category"))
    )

    return JsonResponse(list(data), safe=False)


# COMPLETION COUNTS
@login_required
def report_completions(request):
    completed = Goal.objects.filter(user=request.user, status="Completed").count()
    pending = Goal.objects.filter(user=request.user).exclude(
        status="Completed"
    ).count()

    return JsonResponse(
        {
            "completed": completed,
            "pending": pending,
        }
    )