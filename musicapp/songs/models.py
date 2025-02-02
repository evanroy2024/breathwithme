from django.db import models

class Song(models.Model):
    SCALE_CHOICES = [
        ('quarter', '1/4 Note'),
        ('half', '1/2 Note'),
        ('three_quarter', '3/4 Note'),
        ('full', 'Full Note'),
    ]

    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='songs/')
    vibration_pattern = models.CharField(max_length=20, choices=SCALE_CHOICES, help_text="Choose the vibration pattern based on the music scale")

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
