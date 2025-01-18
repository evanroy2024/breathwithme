from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MusicTrack(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100, default='By admin')
    file = models.FileField(upload_to='music/')
    viewcount = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='tracks', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Connect playlist to user
    name = models.CharField(max_length=255)
    tracks = models.ManyToManyField(MusicTrack, related_name='playlists')  # Many-to-many relationship

    def __str__(self):
        return self.name