from django.urls import path
from . import views
urlpatterns = [
    path('main/', views.course_list, name='course_main'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/results/<int:quiz_id>/', views.quiz_results, name='quiz_results'),
    # path('video/', views.Video, name='video'),

]
