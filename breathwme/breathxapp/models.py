from django.db import models

class SilentExercise(models.Model):
    SHAPE_CHOICES = [
        ('Circle', 'Circle'),
        ('Square', 'Square'),
        ('Rectangle', 'Rectangle'),
        ('Triangle', 'Triangle'),
    ]
    
    name = models.CharField(max_length=255)
    total_time = models.PositiveIntegerField(help_text="Total duration in seconds (e.g., 120 for 2 minutes)")
    breaths = models.PositiveIntegerField()
    skill_level = models.CharField(max_length=15, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    shape = models.CharField(max_length=15, choices=SHAPE_CHOICES, help_text="Shape associated with the vibration cue")
    vibration_cues = models.CharField(max_length=255, help_text="Enter vibration cues as comma-separated values (e.g., 10, 20, 25)",blank=True,null=True)
    vibration_pattern = models.CharField(
        max_length=20,
        blank=True,  # Allow it to be empty if timestamps are used
        null=True,
        help_text="Choose the vibration pattern based on the music scale"
    )
    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User


class SilentSaveExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    shape = models.CharField(max_length=50)
    inputs = models.TextField()  # Store timing as JSON

    def __str__(self):
        return f"{self.nickname} - {self.user.username}"


from django.db import models
from django.contrib.auth.models import User  # Import User model

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings") 
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    
    # Admin fields
    zoom_link = models.URLField(blank=True, null=True)
    admin_message = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"


# Making the admin user uploads strart --------------------------------------------

from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50, choices=[
        ('Beginner', 'Beginner'),
        ('Medium', 'Medium'),
        ('Advanced', 'Advanced')
    ])

    def __str__(self):
        return self.name

class ExercisePhase(models.Model):
    SHAPE_CHOICES = [
        ('Circle', 'Circle'),
        ('Square', 'Square'),
        ('Rectangle', 'Rectangle'),
        ('Triangle', 'Triangle'),
        ('Oval', 'Oval'),
        ('ReversedTriangle', 'ReversedTriangle'),  
        ('Quadrilateral','Quadrilateral')
    ]


    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="phases")
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES)
    bpm = models.PositiveIntegerField(null=True, blank=True)  # Optional, since hold phases don't need BPM
    duration = models.PositiveIntegerField(default=1, help_text="Duration in minutes (minimum 1)")
    hold_time = models.PositiveIntegerField(default=0, help_text="Time to hold breath (in seconds, 0 if none)")

    def clean(self):
        """Ensure duration is at least 1 minute."""
        from django.core.exceptions import ValidationError
        if self.duration < 1:
            raise ValidationError({'duration': 'Duration must be at least 1 minute.'})

    def __str__(self):
        return f"{self.exercise.name} - {self.shape} ({self.duration} min)"

# Making admin user uploads End ----------------------------------------------------