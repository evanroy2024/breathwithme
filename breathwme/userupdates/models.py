from django.db import models

class Notifications(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='notifications_images/', blank=True, null=True)

    def __str__(self):
        return self.title or "Untitled Notification"
