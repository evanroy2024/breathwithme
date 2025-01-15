from django.db import models

class PersonalData(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    hobby = models.TextField(blank=True, null=True)
    favourite_artist = models.CharField(max_length=100, blank=True, null=True)
    goal = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name or "Unnamed Person"
