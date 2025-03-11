from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    total_time_spent = models.DurationField(default=timedelta())

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.total_time_spent}"
