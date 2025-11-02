from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    stats = {
        "total_goals": 12,
        "completed_goals": 8,
        "achievements": 15,
        "streak": 7,
    }

    recent_goals = [
        {"id": 1, "title": "Finish reading a book", "status": "Completed", "progress": 100},
        {"id": 2, "title": "Exercise daily", "status": "In Progress", "progress": 65},
        {"id": 3, "title": "Start journaling", "status": "In Progress", "progress": 40},
    ]

    recent_achievements = [
        {"id": 1, "title": "First Goal Completed", "date": "2 days ago"},
        {"id": 2, "title": "7-Day Streak", "date": "1 week ago"},
        {"id": 3, "title": "Goal Setter", "date": "2 weeks ago"},
    ]

    context = {
        "stats": stats,
        "recent_goals": recent_goals,
        "recent_achievements": recent_achievements,
    }
    return render(request, "dashboard.html", context)
