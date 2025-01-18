from django.shortcuts import render
from .models import MusicTrack , Playlist
from .models import Category


def sleep_program(request):
    # Fetch all categories
    categories = Category.objects.all()

    # If a category is selected, filter tracks by that category
    category_id = request.GET.get('category', None)
    if category_id:
        tracks = MusicTrack.objects.filter(category_id=category_id)
    else:
        tracks = MusicTrack.objects.all()

    return render(request, 'musicapp/sleep_program.html', {
        'tracks': tracks,
        'categories': categories
    })

from django.shortcuts import render
from .models import MusicTrack

def music_list(request):
    tracks = MusicTrack.objects.all()
    return render(request, 'myapp/music_player.html', {'tracks': tracks})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import MusicTrack, Playlist

@login_required
def all_musics(request):
    playlists = Playlist.objects.filter(user=request.user)  # Get playlists for the logged-in user
    selected_playlist = None
    tracks = MusicTrack.objects.all()  # Default to showing all tracks

    # Check if a playlist is selected
    playlist_id = request.GET.get('playlist')
    if playlist_id:
        selected_playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        tracks = selected_playlist.tracks.all()  # Get tracks in the selected playlist

    return render(request, 'musicapp/all_musics.html', {
        'tracks': tracks,
        'playlists': playlists,
        'selected_playlist': selected_playlist,
    })

# Creating play list Start 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Playlist, MusicTrack


# View to create a playlist
@login_required
def create_playlist(request):
    if request.method == 'POST':
        playlist_name = request.POST.get('name')
        if playlist_name:
            playlist = Playlist.objects.create(
                name=playlist_name,
                user=request.user  # Link playlist to the logged-in user
            )
            return redirect('musicapp:view_playlist', playlist_id=playlist.id)  # Redirect to view the playlist
    return render(request, 'musicapp/playlist/create_playlist.html')

# View to add tracks to the playlist
@login_required
def add_tracks_to_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    tracks = MusicTrack.objects.all()  # Get all available tracks

    if request.method == 'POST':
        selected_tracks = request.POST.getlist('tracks')  # Get list of selected tracks
        for track_id in selected_tracks:
            track = get_object_or_404(MusicTrack, id=track_id)
            playlist.tracks.add(track)
        return redirect('musicapp:view_playlist', playlist_id=playlist.id)

    return render(request, 'musicapp/playlist/add_tracks_to_playlist.html', {'playlist': playlist, 'tracks': tracks})

# View to see the playlist and its tracks
@login_required
def view_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    return render(request, 'musicapp/playlist/view_playlist.html', {'playlist': playlist})

# View to display all playlists
@login_required
def all_playlists(request):
    playlists = Playlist.objects.filter(user=request.user)  # Only show playlists created by the user
    return render(request, 'musicapp/playlist/all_playlists.html', {'playlists': playlists})


# # try 
# from django.shortcuts import render, get_object_or_404
# from .models import Playlist, MusicTrack

# # View for listing all playlists of a user
# def playlist_list(request):
#     playlists = Playlist.objects.filter(user=request.user)
#     return render(request, 'musicapp/try/playlist_list.html', {'playlists': playlists})

# # View for displaying tracks in a selected playlist
# def playlist_detail(request, playlist_id):
#     playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
#     tracks = playlist.tracks.all()
#     return render(request, 'musicapp/try/playlist_detail.html', {'playlist': playlist, 'tracks': tracks})
