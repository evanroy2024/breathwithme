from django.shortcuts import render, redirect
from userdata.models import HabitPreference
from django.contrib.auth.decorators import login_required

@login_required
def build_habit(request):
    if request.method == "POST":
        experience = request.POST.get("experience")
        practice_frequency = request.POST.get("practice_frequency")
        preferred_time = request.POST.get("preferred_time")
        allow_notifications = request.POST.get("allow_notifications")
        goal = request.POST.get("goal")

        habit, created = HabitPreference.objects.get_or_create(user=request.user)
        habit.experience = experience
        habit.practice_frequency = practice_frequency
        habit.preferred_time = preferred_time
        habit.allow_notifications = allow_notifications
        habit.goal = goal
        habit.save()

        return redirect('home')  # Redirect after saving

    return render(request, 'breathxapp/habit_form.html')

from django.shortcuts import render
from django.http import JsonResponse
from .models import SilentExercise
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import SilentExercise

def exercise_list(request):
    """Display the list of all exercises."""
    exercises = SilentExercise.objects.all()
    return render(request, 'breathxapp/exercise_list.html', {'exercises': exercises})

from musicapp.models import MusicTrack
def play_exercise(request, exercise_id):
    """Fetch exercise details and return JSON response."""
    exercise = get_object_or_404(SilentExercise, id=exercise_id)
    tracks = MusicTrack.objects.all()
    vibration_patterns = {track.title: track.get_vibration_pattern() for track in tracks}
    print(exercise.breaths)
    return render(request, 'breathxapp/play_exercise.html', {
        'exercise': exercise,
        'tracks': tracks,
        'vibration_patterns': vibration_patterns,
    })




# MEtting booking start here --------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from .models import Booking

def book_meeting(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        date = request.POST.get("date")
        time = request.POST.get("time")

        Booking.objects.create(
            name=name,
            email=email,
            message=message,
            date=date,
            time=time
        )
        return redirect("breathxapp:my_bookings")  # Redirect to my bookings page after booking

    return render(request, "breathxapp/book_meeting.html")

from django.shortcuts import render
from .models import Booking
from django.contrib.auth.decorators import login_required

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user, is_approved=True)  # Get all approved bookings for the logged-in user

    return render(request, "breathxapp/my_bookings.html", {"bookings": bookings})

def activaty(request):
    return render(request, "breathxapp/activaty.html")

# MEtting booking ends here ---------------------------------------------------------------------------------