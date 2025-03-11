# walkapp/urls.py

from django.urls import path
from .views import main_page
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('theme1/', views.theme1, name='theme1'),
    path('signin/', views.signin, name='signin'),  
    path('register/', views.register, name='register'), 
    path('otp_varify/', views.otp_varify, name='otp_varify'), 
    path('logout/', views.user_logout, name='logout'),

    path('home/', views.home, name='home'), 
    path('library/', views.library, name='library'),
    # path('sleep/', views.sleep, name='sleep'),

    path('mainpage/', views.main_page_course, name='main_page_course'),
    path('tracker/', views.tracker, name='tracker'),
    path('profile/', views.profile, name='profile'),
    path('language/', views.language, name='language'),
    path('sequrity/', views.sequrity, name='sequrity'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('paypal/create_payment/<int:plan_id>/', views.create_payment, name='create_payment'),
    path('paypal/execute/', views.execute_payment, name='execute_payment'),


    path('music_player/', views.music_player, name='music_player'),
    path('subscription-expired/', views.subscription_expired, name='subscription_expired'),


]
