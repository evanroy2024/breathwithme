from django.contrib import admin
from .models import Notifications

admin.site.register(Notifications)

from django.contrib import admin
from .models import EmailNotification

@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sent_at')

from django.contrib import admin
from .models import PushNotificationMessage

# userupdates/admin.py

from django.contrib import admin
from .models import PushNotificationMessage, PushNotifications

@admin.register(PushNotificationMessage)
class PushNotificationMessageAdmin(admin.ModelAdmin):
    # no override of save_model or save_related
    pass

@admin.register(PushNotifications)
class PushNotificationsAdmin(admin.ModelAdmin):
    pass




# For testing Firebase FCM --------------------------------------------------------------------------------- 


# notifications/admin.py
from django.contrib import admin
from django.utils import timezone
from .models import DeviceToken, Notification

import os
import firebase_admin
from firebase_admin import credentials, messaging

# Set absolute path to your firebase service account JSON file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
firebase_key_path = os.path.join(BASE_DIR, 'userupdates', 'trialapp-9e25d-firebase-adminsdk-fbsvc-668162cedc.json')

cred = credentials.Certificate(firebase_key_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

@admin.action(description='Send selected notifications')
def send_notifications(modeladmin, request, queryset):
    tokens = list(DeviceToken.objects.values_list('token', flat=True))
    if not tokens:
        modeladmin.message_user(request, "No device tokens found.")
        return

    for notification in queryset:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.body,
                image=notification.image if notification.image else None,
            ),
            tokens=tokens,
        )
        response = messaging.send_multicast(message)
        notification.sent_at = timezone.now()
        notification.save()
        modeladmin.message_user(
            request,
            f"Notification '{notification.title}' sent. Success: {response.success_count}, Failures: {response.failure_count}"
        )

@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'sent_at')
    actions = [send_notifications]
