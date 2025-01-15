from django.urls import path
from . import views
from . views import Video
urlpatterns = [
    path('main/', views.course_list, name='course_main'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('video/', views.Video, name='video'),

]
