from django.contrib import admin
from .models import Milestone, UserMilestone

admin.site.register(Milestone)
admin.site.register(UserMilestone)