from django.contrib import admin
from .models import Category, MusicTrack

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(MusicTrack)
class MusicTrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category')
    list_filter = ('category',)
    search_fields = ('title', 'artist')
