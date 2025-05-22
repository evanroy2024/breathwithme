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
