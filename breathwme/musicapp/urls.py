from django.urls import path
from . import views

urlpatterns = [
    path('sleep-program/', views.sleep_program, name='sleep_program'),
    path('music/', views.music_list, name='music_list'),

]
