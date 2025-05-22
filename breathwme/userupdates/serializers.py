from rest_framework import serializers
from .models import PushNotifications

class PushNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotifications
        fields = ['token']

# serializers.py
from rest_framework import serializers
from mainapp.models import SubscriptionPlan ,  Subscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'description', 'price', 'duration']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'plan', 'payment_status', 'payment_transaction_id', 'start_date', 'end_date']