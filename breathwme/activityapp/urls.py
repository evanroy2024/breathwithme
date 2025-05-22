# urls.py
from django.urls import path
from .views import track_activity

app_name = 'activatyapp'

urlpatterns = [
    path("track-activity/", track_activity, name="track-activity"),
]
