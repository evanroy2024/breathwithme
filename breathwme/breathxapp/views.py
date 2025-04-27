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

from django.shortcuts import render, get_object_or_404
from .models import Exercise

def exercise_list(request):
    """Display all exercises."""
    exercises = Exercise.objects.all()
    return render(request, 'breathxapp/exercise_list.html', {'exercises': exercises})

# def play_exercise(request, exercise_id):
#     """Display a single exercise with all its phases."""
#     exercise = get_object_or_404(Exercise, id=exercise_id)
#     phases = exercise.phases.all()  # related_name="phases" in ForeignKey

#     context = {
#         'exercise': exercise,
#         'phases': phases
#     }
#     return render(request, 'breathxapp/play_exercise.html', context)
# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Exercise, ExercisePhase

# def exercise_list(request):
#     """View to list all exercises"""
#     exercises = Exercise.objects.all()
#     return render(request, 'breathxapp/exercises/exercise_list.html', {'exercises': exercises})

def play_exercise(request, exercise_id):
    """View to play/visualize a specific exercise"""
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    phases = exercise.phases.all()
    
    # Convert phases data to JSON-friendly format for JavaScript
    phases_data = []
    for phase in phases:
        # Get breathing phases based on shape
        breathing_phases = get_breathing_phases_for_shape(phase.shape)
        
        # Collect the input values based on shape
        inputs = [phase.input1, phase.input2, phase.input3, phase.input4]
        
        # Only include valid inputs based on shape
        locked_inputs = phase.get_locked_inputs()
        valid_inputs = []
        for i, value in enumerate(inputs):
            if i not in locked_inputs and value is not None:
                valid_inputs.append(value)
        
        phases_data.append({
            'id': phase.id,
            'shape': phase.shape,
            'inputs': valid_inputs,
            'hold_time': phase.hold_time,
            'cycles': phase.cycles,
            'breathing_phases': breathing_phases
        })
    
    return render(request, 'breathxapp/exercises/exercise_play.html', {
        'exercise': exercise,
        'phases_data': phases_data
    })

def get_breathing_phases_for_shape(shape):
    """Helper function to get breathing phases for each shape"""
    phases_map = {
        'Circle': ["Inhale", "Exhale"],
        'Square': ["Inhale", "Hold", "Exhale", "Hold"],
        'Oval': ["Inhale", "Exhale"],
        'Rectangle': ["Inhale", "Hold", "Exhale", "Hold"],
        'Triangle': ["Inhale", "Exhale", "Hold"],
        'ReversedTriangle': ["Inhale", "Hold", "Exhale"],
        'Quadrilateral': ["Inhale", "Hold", "Exhale", "Hold"]
    }
    return phases_map.get(shape, [])

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

def breathfree(request):
    return render(request, "breathxapp/breathfree.html")


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SilentSaveExercise

@login_required
def save_exercise(request):
    if request.method == "POST":
        try:
            user = request.user
            nickname = request.POST.get("nickname")
            shape = request.POST.get("shape")
            inputs = request.POST.get("inputs")

            if not nickname or not shape or not inputs:
                return JsonResponse({"error": "Missing data"}, status=400)

            SilentSaveExercise.objects.create(
                user=user,
                nickname=nickname,
                shape=shape,
                inputs=inputs
            )

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


from django.shortcuts import render
from .models import SilentSaveExercise

def usersavedexercise(request):
    """ Fetch all exercises saved by the logged-in user """
    if not request.user.is_authenticated:
        return render(request, "usersavedexercise.html", {"exercises": []})

    exercises = SilentSaveExercise.objects.filter(user=request.user)  # FIXED
    return render(request, "breathxapp/usersavedexercise.html", {"exercises": exercises})

from django.shortcuts import render, get_object_or_404
from .models import SilentSaveExercise

def view_saved_exercise(request, exercise_id):
    exercise = get_object_or_404(SilentSaveExercise, id=exercise_id, user=request.user)
    return render(request, "breathxapp/view_saved_exercise.html", {"exercise": exercise})

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

@login_required
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(SilentSaveExercise, id=exercise_id, user=request.user)
    exercise.delete()
    return redirect('breathxapp:usersavedexercise')

# Making admin user uploads Start ----------------------------------------------------
from django.shortcuts import render
from .models import Exercise

def exercise_overview(request):  # Unique view name
    exercises = Exercise.objects.prefetch_related("phases").all()
    return render(request, "breathxapp/test/exercise_list.html", {"exercises": exercises})

# Making admin user uploads End ----------------------------------------------------

def circle_guide(request):
    return render(request, "breathxapp/guide/circle.html")

def square_guide(request):
    return render(request, "breathxapp/guide/square.html")

def rectangle_guide(request):
    return render(request, "breathxapp/guide/rectangle.html")

def oval_guide(request):
    return render(request, "breathxapp/guide/oval.html")

def triangle_guide(request):
    return render(request, "breathxapp/guide/triangle.html")

def reverse_triangle_guide(request):
    return render(request, "breathxapp/guide/reverse_triangle.html")

def diamond_guide(request):
    return render(request, "breathxapp/guide/diamond.html")