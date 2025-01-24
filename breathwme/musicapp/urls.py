from django.urls import path
from . import views
app_name = 'musicapp'
urlpatterns = [
    path('sleep-program/', views.sleep_program, name='sleep_program'),
    path('music/', views.music_list, name='music_list'),
    path('all-musics/', views.all_musics, name='all_musics'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('playlist/<int:playlist_id>/', views.view_playlist, name='view_playlist'),
    path('playlist/<int:playlist_id>/add_tracks/', views.add_tracks_to_playlist, name='add_tracks_to_playlist'),
    path('all_playlists/', views.all_playlists, name='all_playlists'),
]
