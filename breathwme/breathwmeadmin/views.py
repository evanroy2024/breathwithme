import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from musicapp.models import MusicTrack, Category

def upload_music(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        artist = request.POST.get('artist', 'By admin').strip()
        category_id = request.POST.get('category')
        vibration_pattern = request.POST.get('vibration_pattern', '').strip()
        vibrationset = request.POST.get('vibrationset', 'Default')  # Get vibrationset value
        timestamps = request.POST.get('timestamps', '').strip()
        file = request.FILES.get('file')

        # Validate required fields
        if not title or not category_id or not file:
            return JsonResponse({'error': 'Title, category, and file are required!'}, status=400)

        # Ensure only one option is selected
        if vibration_pattern and timestamps:
            return JsonResponse({'error': 'Choose either a vibration pattern or timestamps, not both!'}, status=400)

        # Validate file type
        allowed_extensions = {'mp3', 'wav', 'aac'}
        file_extension = file.name.split('.')[-1].lower()
        if file_extension not in allowed_extensions:
            return JsonResponse({'error': 'Invalid file format! Only MP3, WAV, and AAC are allowed.'}, status=400)

        # Efficient file saving (avoid overwriting)
        file_path = f"music/{file.name}"
        if default_storage.exists(file_path):
            file_path = f"music/{file.name.split('.')[0]}_{file.size}.{file_extension}"

        default_storage.save(file_path, ContentFile(file.read()))

        # Fetch category efficiently
        category = get_object_or_404(Category, id=category_id)

        # Save track
        track = MusicTrack.objects.create(
            title=title,
            artist=artist,
            file=file_path,
            vibration_pattern=vibration_pattern or None,
            timestamps=timestamps or None,
            vibrationset=vibrationset,  # Save vibrationset
            category=category
        )

        return JsonResponse({'message': 'Track uploaded successfully!', 'track_id': track.id}, status=201)

    # Fetch categories
    categories = Category.objects.only('id', 'name')

    return render(request, 'admintemplate/upload_music.html', {'categories': categories})
