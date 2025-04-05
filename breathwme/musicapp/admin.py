from django.contrib import admin
from .models import Category, MusicTrack , Playlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin
from .models import MusicTrack

from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from .models import MusicTrack

@admin.register(MusicTrack)
class MusicTrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'viewcount', 'vibration_pattern', 'category', 'image','vibrationset','bpm')
    search_fields = ('title', 'artist')
    list_filter = ('vibration_pattern', 'category')
    ordering = ('-viewcount',)
    change_list_template = "admin/musictrack/change_list.html"  # Custom template for adding a button


admin.site.register(Playlist)




from .models import GlobalPlaylist
@admin.register(GlobalPlaylist)
class GlobalPlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    filter_horizontal = ('tracks',)
