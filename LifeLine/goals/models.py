from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    STATUS_CHOICES = [
        ("Not Started", "Not Started"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    CATEGORY_CHOICES = [
    ("Personal Development", "Personal Development"),
    ("Health & Fitness", "Health & Fitness"),
    ("Learning", "Learning"),
    ("Career", "Career"),
    ("Finance", "Finance"),
    ("Relationships", "Relationships"),
    ("Hobbies", "Hobbies"),
    ("Travel", "Travel"),
    ("Other", "Other"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(
    max_length=100,
    choices=CATEGORY_CHOICES,
    default="Other"
)

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


class Milestone(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    required_value = models.PositiveIntegerField()  # Target for unlock
    milestone_type = models.CharField(
        max_length=50,
        choices=[
            ("total_goals", "Total Goals"),
            ("completed_goals", "Completed Goals"),
            ("progress", "Progress"),
            ("category", "Category"),
        ]
    )

    category = models.CharField(
        max_length=100,
        choices=Goal.CATEGORY_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class UserMilestone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)
    unlocked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "milestone")
        indexes = [
            models.Index(fields=["user", "milestone"]),
        ]


class GoalProgressLog(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
