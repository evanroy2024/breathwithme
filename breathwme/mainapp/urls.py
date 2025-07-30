# walkapp/urls.py

from django.urls import path
from .views import main_page
from . import views

urlpatterns = [
    path('theme1/', views.main_page, name='main_page'),
    path('app/', views.app_main_page, name='app_main_page'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('', views.theme1, name='theme1'),
    path('login/', views.signin, name='signin'),  
    path('register/', views.register, name='register'), 
    path('otp_varify/', views.otp_varify, name='otp_varify'), 
    path('logout/', views.user_logout, name='logout'),

    path('forget-password/', views.forget_password, name='forget_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    path('terms/', views.terms_and_conditions, name='terms'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('liability/', views.liability, name='liability'),
    path('home/', views.home, name='home'), 
    path('playlist/', views.library, name='library_list'),
    path('library_list/', views.library_list, name='library'),

    # path('sleep/', views.sleep, name='sleep'),

    path('mainpage/', views.main_page_course, name='main_page_course'),
    path('tracker/', views.tracker, name='tracker'),
    path('profile/', views.profile, name='profile'),
    path('language/', views.language, name='language'),
    path('sequrity/', views.sequrity, name='sequrity'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    # In urls.py, add this pattern
    path('free_subscription/<int:plan_id>/', views.free_subscription, name='free_subscription'),          # When proce is 0 
    path('paypal/create_payment/<int:plan_id>/', views.create_payment, name='create_payment'),
    path('paypal/execute/', views.execute_payment, name='execute_payment'),


    path('music_player/', views.music_player, name='music_player'),
    path('subscription-expired/', views.subscription_expired, name='subscription_expired'),

    path('user-subscription/', views.user_subscription_page, name='user_subscription_page'),

    # Settings 
    path('push-notifications/', views.user_push_notifications, name='user_push_notifications'),
    path('email-notifications/', views.user_email_notifications, name='user_email_notifications'),
    path('user-privacy-settings/', views.user_privacy_settings, name='user_privacy_settings'),
    path('delete-account/', views.delete_account, name='delete_account'),


]
