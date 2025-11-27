from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("list/", views.goals_page, name="goals_page"),
    path("create/", views.create_goal, name="create_goal"),
    path("update-progress/<int:pk>/", views.update_progress, name="update_progress"),
    path("<int:pk>/delete/", views.delete_goal, name="delete_goal"),
]
