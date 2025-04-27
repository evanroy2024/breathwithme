from django.urls import path
from . import views

app_name = 'testapp'

urlpatterns = [
    path('', views.song_list, name='song_list'),
    path('exercise/<int:pk>/', views.exercise_page, name='exercise_page'),
    path('filter_playlists/', views.filter_playlists, name='filter_playlists'),
    path("marking-songs/", views.marking_song_list, name="marking_song_list"),
    path("marking-songs/<int:id>/mark/", views.marking_beats, name="marking_beats"),
    path("marking-songs/<int:id>/save/", views.save_beat_times, name="save_beat_times"),

]

