from django.urls import path
from .views import generate_referral_link, mycoins , extend_subscription

app_name = 'referal'

urlpatterns = [
    path("generate/", generate_referral_link, name="generate_referral_link"),
    path("mycoins/", mycoins, name="mycoins"),
    path("extend-subscription/", extend_subscription, name="extend_subscription"),
]
