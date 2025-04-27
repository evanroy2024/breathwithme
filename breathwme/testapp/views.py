from django.shortcuts import render, get_object_or_404
from .models import TestExercise ,Category

def song_list(request):
    songs = TestExercise.objects.all()
    return render(request, 'testbpm/song_list.html', {'songs': songs})
# def exercise_page(request, pk):
#     selected_song_id = request.GET.get('song_id', pk)
#     song = get_object_or_404(TestExercise, pk=selected_song_id)
#     all_songs = TestExercise.objects.all()
#     return render(request, 'testbpm/exercise_page.html', {'song': song, 'all_songs': all_songs})
from musicapp.models import Playlist

def exercise_page(request, pk):
    # Get the selected song, or use the provided pk as default
    selected_song_id = request.GET.get('song_id', pk)
    song = get_object_or_404(TestExercise, pk=selected_song_id)
    
    # Fetch all categories
    categories = Category.objects.all()
    
    # Fetch all songs
    all_songs = TestExercise.objects.all()
    
    # Fetch the selected category if any
    selected_category_id = request.GET.get('category_id', None)
    if selected_category_id:
        # Filter songs by the selected category
        all_songs = all_songs.filter(category_id=selected_category_id)
    
    # Fetch playlists for the logged-in user (if needed)
    playlists = Playlist.objects.filter(user=request.user)
    
    # Handle AJAX requests to update song list dynamically
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        song_options = []
        for s in all_songs:
            # Include the full HTML structure with all CSS classes for styling
            song_options.append(f'''
            <div class="dark-song-item">
                <a href="?song_id={s.id}&category_id={selected_category_id or ''}" class="dark-song-link">
                    <div class="dark-song-icon">♫</div>
                    <div class="dark-song-title">{s.title}</div>
                    <div class="dark-song-arrow">→</div>
                </a>
            </div>
            ''')
        return JsonResponse({'song_options': song_options})
    
    # Return the rendered page
    return render(request, 'testbpm/exercise_page.html', {
        'song': song,
        'all_songs': all_songs,
        'categories': categories,
        'playlists': playlists,
        'selected_category_id': selected_category_id,  # Pass this to the template
    })
def filter_playlists(request):
    category_id = request.GET.get('category_id')
    if category_id:
        playlists = Playlist.objects.filter(tracks__category_id=category_id, user=request.user)
    else:
        playlists = Playlist.objects.filter(user=request.user)
    
    playlist_data = [{'id': playlist.id, 'name': playlist.name} for playlist in playlists]
    return JsonResponse({'playlists': playlist_data})
# Marking view 
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import TestExercise

def marking_song_list(request):
    songs = TestExercise.objects.all()
    return render(request, "testbpm/marking_song_list.html", {"songs": songs})

def marking_beats(request, id):
    song = get_object_or_404(TestExercise, id=id)
    return render(request, "testbpm/manual_marker.html", {"song": song})

@csrf_exempt
def save_beat_times(request, id):
    if request.method == "POST":
        song = get_object_or_404(TestExercise, id=id)
        data = json.loads(request.body)
        beat_times = data.get("beat_times", [])
        song.beat_times = beat_times
        song.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail"}, status=400)

