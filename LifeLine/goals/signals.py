from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Goal, Milestone, UserMilestone


@receiver(post_save, sender=Goal)
def check_milestones(sender, instance, **kwargs):
    user = instance.user

    # Total and completed goals
    total_goals = Goal.objects.filter(user=user).count()
    completed_goals = Goal.objects.filter(user=user, status="Completed").count()

    # All goals for progress checking
    user_goals = Goal.objects.filter(user=user)

    for milestone in Milestone.objects.all():
        # Get or create UserMilestone
        user_m, _ = UserMilestone.objects.get_or_create(user=user, milestone=milestone)
        if user_m.unlocked:
            continue  # Skip already unlocked

        achieved = False

        if milestone.milestone_type == "total_goals":
            achieved = total_goals >= milestone.required_value

        elif milestone.milestone_type == "completed_goals":
            achieved = completed_goals >= milestone.required_value

        elif milestone.milestone_type == "progress":
            # Unlock if any goal has progress >= required_value
            achieved = user_goals.filter(progress__gte=milestone.required_value).exists()

        # elif milestone.milestone_type == "category" and milestone.category:
        #     # Count only goals in that category that are started or completed
        #     count_in_category = user_goals.filter(
        #         category=milestone.category,
        #         progress__gt=0  # Only consider goals with some progress
        #     ).count()
        #     achieved = count_in_category >= milestone.required_value

        elif milestone.milestone_type == "category" and milestone.category:
            # Count goals in that category
            count_in_category = Goal.objects.filter(user=user, category=milestone.category).count()
            achieved = count_in_category >= milestone.required_value

        if achieved:
            user_m.unlocked = True
            user_m.unlocked_at = timezone.now()
            user_m.save()
