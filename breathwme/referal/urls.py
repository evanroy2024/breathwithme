from django.urls import path
from .views import generate_referral_link, mycoins , extend_subscription

from . import views
app_name = 'referal'

urlpatterns = [
    path("generate/", generate_referral_link, name="generate_referral_link"),
    path("mycoins/", mycoins, name="mycoins"),
    path("extend-subscription/", extend_subscription, name="extend_subscription"),
    path("generate-qr/", views.generate_qr_code, name="generate_qr_code"), # Generate QR code 
    path('referral-preview/', views.referral_preview, name='referral_preview'),  # <-- NEW
    

]
