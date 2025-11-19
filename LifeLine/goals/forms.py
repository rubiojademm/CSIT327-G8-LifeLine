from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["title", "description", "category", "target_date"]

class GoalProgressForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ["progress"]
