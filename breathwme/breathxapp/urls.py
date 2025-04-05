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
from .views import save_exercise , usersavedexercise , exercise_overview    

app_name = 'breathxapp'

urlpatterns = [
    path('build-habit/', build_habit, name='build_habit'),

    path('', views.exercise_list, name='exercise_list'),  # List of all exercises
    path('play/<int:exercise_id>/', views.play_exercise, name='play_exercise'),  # Play a specific exercise
    path("book-meeting/", book_meeting, name="book_meeting"),
    path("my-bookings/", my_bookings, name="my_bookings"),  # Ensure this name matches

    path("activaty/", activaty, name="activaty"),  # Ensure this name matches
    path("breathfree/", breathfree, name="breathfree"),  # Ensure this name matches

    path("save-exercise/", save_exercise, name="save_exercise"),
    path("usersavedexercise/", usersavedexercise, name="usersavedexercise"),
    path("view-exercise/<int:exercise_id>/", views.view_saved_exercise, name="view_saved_exercise"),
    path("exercise-overview/", exercise_overview, name="exercise_overview"),  # Unique URL name
    path('exercise/<int:exercise_id>/delete/', views.delete_exercise, name='delete_exercise'),  # 🔥 New

    path("circle_guide/", views.circle_guide, name="circle_guide"),  # Ensure this name matches
    path("square_guide/", views.square_guide, name="square_guide"),
    path("rectangle_guide/", views.rectangle_guide, name="rectangle_guide"),
    path("oval_guide/", views.oval_guide, name="oval_guide"),
    path("triangle_guide/", views.triangle_guide, name="triangle_guide"),
    path("reverse_triangle_guide/", views.reverse_triangle_guide, name="reverse_triangle_guide"),
    path("diamond_guide/", views.diamond_guide, name="diamond_guide"),

]
