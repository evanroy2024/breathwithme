from django.urls import path
from .views import SavePushTokenView ,SubscriptionPlanListAPIView , SubscribeAPIView , SaveTokenView
urlpatterns = [
    path('api/save-token/', SavePushTokenView.as_view(), name='save-push-token'),
    path('api/subscription-plans/', SubscriptionPlanListAPIView.as_view(), name='subscription-plans'),
    path('api/subscribe/', SubscribeAPIView.as_view(), name='subscribe'),
    path('save-token/', SaveTokenView.as_view(), name='save-token'),
]
