# Generated by Django 5.1.5 on 2025-03-06 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breathxapp', '0010_booking_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='silentexercise',
            name='bpm',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
