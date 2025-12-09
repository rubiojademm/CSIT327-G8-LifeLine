from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Goal, GoalProgressLog
from .models import Milestone, UserMilestone


# DASHBOARD PAGE #
@login_required
def dashboard(request):
    user = request.user
    user_goals = Goal.objects.filter(user=user)

    # -------------------------------
    # GOAL STATS
    # -------------------------------
    total_goals = user_goals.count()
    completed_goals = user_goals.filter(status="Completed").count()
    in_progress_goals = user_goals.filter(status="In Progress").count()
    not_started_goals = user_goals.filter(status="Not Started").count()

    completion_rate = (completed_goals / total_goals) * 100 if total_goals > 0 else 0

    # -------------------------------
    # RECENT GOALS
    # -------------------------------
    recent_goals = user_goals.order_by('-created_at')[:3]

    # -------------------------------
    # USER ACHIEVEMENTS ✅ (FIXED)
    # -------------------------------
    user_achievements = UserMilestone.objects.filter(
        user=user,
        unlocked=True
    )

    achievements_count = user_achievements.count()

    recent_achievements = user_achievements.select_related("milestone") \
                                           .order_by('-unlocked_at')[:3]

    # -------------------------------
    # STREAK CALCULATION ✅ (FIXED)
    # -------------------------------
    streak = 0
    today = timezone.now().date()

    completion_dates = user_achievements.values_list("unlocked_at", flat=True)
    completion_set = set([d.date() for d in completion_dates if d])

    while today in completion_set:
        streak += 1
        today -= timedelta(days=1)

    # -------------------------------
    # FINAL STATS
    # -------------------------------
    stats = {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "in_progress_goals": in_progress_goals,
        "not_started_goals": not_started_goals,
        "achievements": achievements_count,
        "streak": streak,
        "completion_rate": round(completion_rate),
    }

    context = {
        "stats": stats,
        "recent_goals": recent_goals,
        "recent_achievements": recent_achievements,
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
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        category = request.POST.get("category", "").strip()
        target_date = request.POST.get("target_date")

        # HARD VALIDATION
        if not title or not description or not category:
            return redirect("goals_page")

        # SAFE DATE CHECK
        parsed_date = None
        if target_date:
            try:
                parsed_date = timezone.datetime.strptime(target_date, "%Y-%m-%d").date()
                today = timezone.now().date()
                max_date = today + timedelta(days=365)

                if parsed_date < today or parsed_date > max_date:
                    parsed_date = None
            except:
                parsed_date = None

        Goal.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            target_date=parsed_date
        )

        return redirect("goals_page")


@login_required
def update_progress(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)

    if request.method == "POST":
        # Update goal progress safely
        try:
            new_progress = int(request.POST.get("progress", goal.progress))
        except ValueError:
            new_progress = goal.progress

        goal.progress = max(0, min(100, new_progress))
        goal.save()

        # Check for newly unlocked milestones
        unlocked = UserMilestone.objects.filter(
            user=request.user,
            unlocked=False,
            milestone__milestone_type="progress",
            milestone__required_value__lte=goal.progress
        )

        # If the milestone has a category, match it with the goal's category
        unlocked = unlocked.filter(
            Q(milestone__category=goal.category) | Q(milestone__category__isnull=True)
        )

        # Unlock the milestones and show messages
        for um in unlocked:
            um.unlocked = True
            um.unlocked_at = timezone.now()
            um.save()
            messages.success(
                request,
                f"🏆 Achievement Unlocked: {um.milestone.title}"
            )

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


# =============================
# ADMIN – VIEW USER GOALS
# =============================
@staff_member_required
def admin_user_goals(request, user_id):
    selected_user = get_object_or_404(User, id=user_id)
    goals = Goal.objects.filter(user=selected_user).order_by("-created_at")

    return render(request, "admin_user_goals.html", {
        "selected_user": selected_user,
        "goals": goals,
    })


# =============================
# ADMIN – DELETE USER GOAL
# =============================
@staff_member_required
def admin_delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    username = goal.user.username
    goal_title = goal.title

    goal.delete()

    messages.success(
        request,
        f"Deleted goal '{goal_title}' from user '{username}'."
    )

    return redirect("admin_dashboard")
