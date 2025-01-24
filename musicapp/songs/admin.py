from django.contrib import admin
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'vibration_pattern')  # Display song title and pattern
    fields = ('title', 'audio_file', 'vibration_pattern')  # Fields for admin form
    list_filter = ('vibration_pattern',)  # Filter songs by vibration pattern
    search_fields = ('title',)  # Search songs by title
