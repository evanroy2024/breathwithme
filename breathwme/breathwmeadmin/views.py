import json
from django.shortcuts import render
from django.http import JsonResponse
from musicapp.models import MusicTrack, Category
from django.core.files.storage import default_storage

def upload_music(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist', 'By admin')
        category_id = request.POST.get('category')
        vibration_pattern = request.POST.get('vibration_pattern')
        timestamps = request.POST.get('timestamps', '')  # Get timestamps as a string
        file = request.FILES.get('file')

        # Ensure only one option is selected
        if vibration_pattern and timestamps:
            return JsonResponse({'error': 'Choose either a vibration pattern or timestamps, not both!'}, status=400)

        # Save file
        if file:
            file_path = default_storage.save(f"music/{file.name}", file)

            # Save track to database
            category = Category.objects.get(id=category_id)
            track = MusicTrack.objects.create(
                title=title,
                artist=artist,
                file=file_path,
                vibration_pattern=vibration_pattern if vibration_pattern else None,
                timestamps=timestamps if timestamps else None,
                category=category
            )

            return JsonResponse({'message': 'Track uploaded successfully!', 'track_id': track.id})

    categories = Category.objects.all()
    tracks = MusicTrack.objects.all()
    return render(request, 'admintemplate/upload_music.html', {'categories': categories, 'tracks': tracks})
