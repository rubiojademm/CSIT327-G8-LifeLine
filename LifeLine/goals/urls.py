from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("list/", views.goals_page, name="goals_page"),
    path("create/", views.create_goal, name="create_goal"),
    path("update-progress/<int:pk>/", views.update_progress, name="update_progress"),
    path("<int:pk>/delete/", views.delete_goal, name="delete_goal"),
    path("milestones/", views.milestones_page, name="milestones_page"),
    path("admin/user-goals/<int:user_id>/", views.admin_user_goals, name="admin_user_goals"),
    path("admin/delete-goal/<int:goal_id>/", views.admin_delete_goal, name="admin_delete_goal"),
]
