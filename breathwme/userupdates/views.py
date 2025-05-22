from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import PushNotificationsSerializer
from .models import PushNotifications
import logging

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class SavePushTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PushNotificationsSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            PushNotifications.objects.update_or_create(token=token)
            return Response({"detail": "Token saved"})
        return Response(serializer.errors, status=400)



# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from mainapp.models import Subscription, SubscriptionPlan

# Serializers
from .serializers import SubscriptionPlanSerializer
from rest_framework.permissions import AllowAny
from .serializers import SubscriptionSerializer

class SubscriptionPlanListAPIView(APIView):
    permission_classes = [AllowAny]  # <-- This disables authentication for this view

    def get(self, request):
        plans = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data)
class SubscribeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        plan_id = request.data.get("plan_id")
        transaction_id = request.data.get("transaction_id")
        payment_status = request.data.get("payment_status", "Completed")

        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "Subscription plan not found"}, status=status.HTTP_404_NOT_FOUND)

        start_date = now().date()
        end_date = start_date + timedelta(days=plan.duration or 30)

        subscription_data = {
            "user": user.id,
            "plan": plan.id,
            "payment_status": payment_status,
            "payment_transaction_id": transaction_id,
            "start_date": start_date,
            "end_date": end_date,
        }

        serializer = SubscriptionSerializer(data=subscription_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Subscription created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)