from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MusicTrack(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100, default='By admin')
    file = models.FileField(upload_to='music/')
    category = models.ForeignKey(Category, related_name='tracks', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
