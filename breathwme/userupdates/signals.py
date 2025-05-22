# import logging
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import PushNotificationMessage, PushNotifications
# from .utils import send_push_notifications

# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=PushNotificationMessage)
# def send_push_notification_on_save(sender, instance, created, **kwargs):
#     print(f"Signal triggered for PushNotificationMessage save: id={instance.id}, created={created}")
#     logger.info(f"Signal triggered for PushNotificationMessage save: id={instance.id}, created={created}")

#     if created and not instance.sent:
#         tokens = list(PushNotifications.objects.values_list('token', flat=True))
#         print(f"Tokens found: {tokens}")
#         logger.info(f"Tokens found: {tokens}")

#         if tokens:
#             success = send_push_notifications(tokens, instance.title, instance.body)
#             print(f"send_push_notifications success: {success}")
#             if success:
#                 instance.sent = True
#                 instance.save(update_fields=['sent'])
#                 print("Notification sent and instance marked sent")
#                 logger.info("Notification sent and instance marked sent")
#             else:
#                 print("Failed to send notifications")
#                 logger.error("Failed to send notifications")
#         else:
#             print("No tokens found to send notifications")
#             logger.warning("No tokens found to send notifications")

# userupdates/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PushNotificationMessage, PushNotifications
from .utils import send_push_notifications

logger = logging.getLogger(__name__)
@receiver(post_save, sender=PushNotificationMessage)
def send_push_notification_on_save(sender, instance, created, **kwargs):
    print(f"Signal triggered for PushNotificationMessage save: {instance.id} created={created} sent={instance.sent}")
    if created and not instance.sent:
        tokens = list(PushNotifications.objects.values_list('token', flat=True))
        print(f"Tokens found: {tokens}")
        if tokens:
            print("About to call send_push_notifications()")
            success = send_push_notifications(tokens, instance.title, instance.body)
            print(f"send_push_notifications() returned: {success}")
            if success:
                instance.sent = True
                instance.save(update_fields=['sent'])
                print("Instance marked as sent")
        else:
            print("No tokens found to send notifications")
    else:
        print("Either not created or already sent, skipping send")
