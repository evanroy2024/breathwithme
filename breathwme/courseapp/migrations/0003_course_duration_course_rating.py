# Generated by Django 5.1.5 on 2025-01-15 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courseapp', '0002_course_end_date_course_image_course_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=5.0, max_digits=2),
        ),
    ]
