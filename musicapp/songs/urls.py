from django.urls import path
from . import views

urlpatterns = [
    path('', views.song_list, name='song_list'),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
]
