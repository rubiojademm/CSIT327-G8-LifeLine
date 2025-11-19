from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    STATUS_CHOICES = [
        ("Not Started", "Not Started"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)

    progress = models.PositiveIntegerField(default=0)  # 0–100
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Not Started")

    created_at = models.DateTimeField(auto_now_add=True)
    target_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-update status based on progress
        if self.progress >= 100:
            self.status = "Completed"
        elif self.progress > 0:
            self.status = "In Progress"
        else:
            self.status = "Not Started"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
