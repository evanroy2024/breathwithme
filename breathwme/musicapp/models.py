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
    VIBRATION_CHOICES = [
    ('Default', 'Default'),
    ('Customise', 'Customise'),
    ]

    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100, default='By admin')
    file = models.FileField(upload_to='music/')
    image = models.ImageField(upload_to="music/images/", blank=True, null=True)
    viewcount = models.IntegerField(default=0)
    bpm = models.IntegerField(default=30,blank=True, null=True)

    vibrationset = models.CharField(max_length=10, choices=VIBRATION_CHOICES, default='Default')
    vibration_pattern = models.CharField(
        max_length=20,
        choices=SCALE_CHOICES,
        blank=True,  # Allow it to be empty if timestamps are used
        null=True,
        help_text="Choose the vibration pattern based on the music scale"
    )

    timestamps = models.TextField(
        blank=True,  # Allow it to be empty if vibration pattern is used
        null=True,
        help_text="Comma-separated timestamps (e.g., 5,14,20)"
    )
    
    category = models.ForeignKey(Category, related_name='tracks', on_delete=models.CASCADE, default=1)

    def get_vibration_pattern(self):
        patterns = {
            'quarter': [200, 100, 200, 100],
            'half': [400, 200, 400, 200],
            'three_quarter': [600, 300, 600, 300],
            'full': [800, 400, 800, 400],
        }
        return patterns.get(self.vibration_pattern, [])

    def get_timestamps(self):
        if self.timestamps:
            try:
                return [float(t.strip()) for t in self.timestamps.split(',')]  # Convert to list of floats
            except ValueError:
                return []  # Handle invalid data gracefully
        return []

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure only one of vibration_pattern or timestamps is selected
        if self.vibration_pattern and self.timestamps:
            raise ValidationError("You can only select a vibration pattern or enter custom timestamps, not both.")
        
    

    def __str__(self):
        return self.title

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Connect playlist to user
    name = models.CharField(max_length=255)
    tracks = models.ManyToManyField(MusicTrack, related_name='playlists')  # Many-to-many relationship

    def __str__(self):
        return self.name
    



# class GlobalPlaylist(models.Model):
#     name = models.CharField(max_length=255)
#     tracks = models.ManyToManyField(MusicTrack, related_name='global_playlists')

#     def __str__(self):
#         return self.name



