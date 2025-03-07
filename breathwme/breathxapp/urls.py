# from django.urls import path
# from . import views

# app_name = 'breathxapp'

# urlpatterns = [
#     path('build-habit/', build_habit, name='build_habit'),
#     path('', views.exercise_list, name='exercise_list'),  # List of all exercises
#     path('play/<int:exercise_id>/', views.play_exercise, name='play_exercise'),
# ]

from django.urls import path
from . import views
from .views import build_habit
from .views import book_meeting, my_bookings , activaty , breathfree

app_name = 'breathxapp'

urlpatterns = [
    path('build-habit/', build_habit, name='build_habit'),

    path('', views.exercise_list, name='exercise_list'),  # List of all exercises
    path('play/<int:exercise_id>/', views.play_exercise, name='play_exercise'),  # Play a specific exercise
    path("book-meeting/", book_meeting, name="book_meeting"),
    path("my-bookings/", my_bookings, name="my_bookings"),  # Ensure this name matches

    path("activaty/", activaty, name="activaty"),  # Ensure this name matches
    path("breathfree/", breathfree, name="breathfree"),  # Ensure this name matches


]
