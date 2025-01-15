from django.shortcuts import render
from .models import MusicTrack
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
