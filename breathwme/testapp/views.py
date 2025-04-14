from django.shortcuts import render, get_object_or_404
from .models import TestExercise

def song_list(request):
    songs = TestExercise.objects.all()
    return render(request, 'testbpm/song_list.html', {'songs': songs})

def exercise_page(request, pk):
    song = get_object_or_404(TestExercise, pk=pk)
    return render(request, 'testbpm/exercise_page.html', {'song': song})


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
