# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class PageVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=500)
    duration_seconds = models.IntegerField(default=0)
    date = models.DateField(default=now)   # Store just the date
    timestamp = models.DateTimeField(auto_now=True)  # last updated time

    def __str__(self):
        return f"{self.user} visited {self.url} for {self.duration_seconds}s on {self.date}"



class DailyUserSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    
    breath_free_page = models.IntegerField(default=0)
    breathx_play_page = models.IntegerField(default=0)
    breath_save_page = models.IntegerField(default=0)
    breathing_beats_page = models.IntegerField(default=0)
    course_page = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"Summary for {self.user} on {self.date}"