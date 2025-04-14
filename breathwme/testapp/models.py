from django.db import models
from django.conf import settings
import os

class TestExercise(models.Model):
    class Meta:
        verbose_name = "Breathing Beats"  # This will change the model name in the admin panel
        verbose_name_plural = "Breathing Beats"  # This will change the plural form

    title = models.CharField(max_length=255)
    song = models.FileField(upload_to='songs/')
    beat_times = models.JSONField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return self.title
