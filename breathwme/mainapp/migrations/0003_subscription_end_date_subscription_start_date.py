# Generated by Django 5.1.5 on 2025-03-10 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
