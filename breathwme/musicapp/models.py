from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MusicTrack(models.Model):
    SCALE_CHOICES = [
        ('quarter', '1/4 Note'),
        ('half', '1/2 Note'),
        ('three_quarter', '3/4 Note'),
        ('full', 'Full Note'),
    ]

    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100, default='By admin')
    file = models.FileField(upload_to='music/')
    viewcount = models.IntegerField(default=0)
    vibration_pattern = models.CharField(max_length=20, choices=SCALE_CHOICES, help_text="Choose the vibration pattern based on the music scale")
    category = models.ForeignKey(Category, related_name='tracks', on_delete=models.CASCADE, default=1)

    def get_vibration_pattern(self):
        patterns = {
            'quarter': [200, 100, 200, 100],  # Example: Short zooms
            'half': [400, 200, 400, 200],     # Example: Longer zooms
            'three_quarter': [600, 300, 600, 300],  # Example: Extended zooms
            'full': [800, 400, 800, 400],     # Example: Full zooms
        }
        return patterns.get(self.vibration_pattern, [])

    def __str__(self):
        return self.title

    def __str__(self):
        return self.title

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Connect playlist to user
    name = models.CharField(max_length=255)
    tracks = models.ManyToManyField(MusicTrack, related_name='playlists')  # Many-to-many relationship

    def __str__(self):
        return self.name
    







