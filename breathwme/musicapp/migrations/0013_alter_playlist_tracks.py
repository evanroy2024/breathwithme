# Generated by Django 5.1.5 on 2025-04-25 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0012_remove_globalplaylist_created_at'),
        ('testapp', '0004_category_testexercise_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(related_name='playlists', to='testapp.testexercise'),
        ),
    ]
