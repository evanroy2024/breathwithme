from django.shortcuts import render, get_object_or_404
from .models import Song

def song_list(request):
    songs = Song.objects.all()
    return render(request, 'songs/song_list.html', {'songs': songs})

def play_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    vibration_pattern = song.get_vibration_pattern()
    return render(request, 'songs/play_song.html', {'song': song, 'vibration_pattern': vibration_pattern})
