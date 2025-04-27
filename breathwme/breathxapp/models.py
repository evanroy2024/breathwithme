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

from django.db import models
from django.core.exceptions import ValidationError

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
        ('Circle', 'Circle (1)'),
        ('Square', 'Square (1)'),
        ('Rectangle', 'Rectangle (2)'),
        ('Triangle', 'Triangle (3)'),
        ('Oval', 'Oval (2)'),
        ('ReversedTriangle', 'ReversedTriangle (4)'),
        ('Quadrilateral', 'Quadrilateral (4)')
    ]

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="phases")
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES)

    # Replacing bpm with 4 input fields
    input1 = models.PositiveIntegerField(null=True, blank=True)
    input2 = models.PositiveIntegerField(null=True, blank=True)
    input3 = models.PositiveIntegerField(null=True, blank=True)
    input4 = models.PositiveIntegerField(null=True, blank=True)

    hold_time = models.PositiveIntegerField(default=0, help_text="Time to hold breath (in seconds, 0 if none)")

    # New field for cycles
    cycles = models.PositiveIntegerField(default=1, help_text="Number of cycles to complete (minimum 1)")

    def clean(self):
        """Ensure shape-based input restrictions."""
        locked_inputs = self.get_locked_inputs()
        inputs = [self.input1, self.input2, self.input3, self.input4]

        for i, value in enumerate(inputs):
            if i in locked_inputs and value is not None:
                raise ValidationError({f'input{i+1}': 'This field is locked and must remain empty.'})

        # Validate cycles to ensure it's at least 1
        if self.cycles < 1:
            raise ValidationError({'cycles': 'The number of cycles must be at least 1.'})

    def get_locked_inputs(self):
        """Returns which inputs should be locked based on shape selection."""
        shape_locks = {
            'Circle': [ 2, 3],
            'Square': [1, 2, 3],
            'Rectangle': [3, 4],  # Lock input3 and input4 for Rectangle (allow input1 and input2)
            'Quadrilateral': [],
            'Triangle': [3],
            'ReversedTriangle': [3],
            'Oval': [2, 3]
        }
        return shape_locks.get(self.shape, [])

    def __str__(self):
        return f"{self.exercise.name} - {self.shape} - Cycles: {self.cycles}"

# Making admin user uploads End ----------------------------------------------------