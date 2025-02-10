from django.db import models
from django.contrib.auth.models import User

class Userdata(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userdata")
    name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    hobby = models.TextField(blank=True, null=True)
    favourite_artist = models.CharField(max_length=100, blank=True, null=True)
    goal = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)


    def __str__(self):
        return self.name or "Unnamed Userdata"


from django.db import models
from django.contrib.auth.models import User

class HabitPreference(models.Model):
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    FREQUENCY_CHOICES = [
        ('1', 'Once a week'),
        ('2', 'Twice a week'),
        ('3', 'Three times a week'),
        ('4', 'Four times a week'),
        ('5', 'Five times a week'),
        ('6', 'Six times a week'),
        ('7', 'Every day'),
    ]
    
    TIME_OF_DAY_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
        ('night', 'Night'),
    ]
    
    NOTIFICATION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    GOAL_CHOICES = [
        ('relaxation', 'Relaxation'),
        ('focus', 'Better focus'),
        ('sleep', 'Improve sleep'),
        ('stress', 'Reduce stress'),
        ('energy', 'Increase energy'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    practice_frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    preferred_time = models.CharField(max_length=20, choices=TIME_OF_DAY_CHOICES)
    allow_notifications = models.CharField(max_length=5, choices=NOTIFICATION_CHOICES)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)

    def __str__(self):
        return f"{self.user.username}'s Habit Preferences"
