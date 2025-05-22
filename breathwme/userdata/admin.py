from django.contrib import admin
from .models import Userdata
admin.site.register(Userdata)



from django.contrib import admin
from .models import HabitPreference

@admin.register(HabitPreference)
class HabitPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'practice_frequency', 'preferred_time', 'allow_notifications', 'goal')
    list_filter = ('experience', 'practice_frequency', 'preferred_time', 'goal')


from django.contrib import admin
from .models import UserSettingsPreference

@admin.register(UserSettingsPreference)
class UserSettingsPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'email_notification',
        'push_notification',
        'visibility',
        'data_access',
        'activity_access',
    )
    list_filter = (
        'email_notification',
        'push_notification',
        'visibility',
        'data_access',
        'activity_access',
    )
    search_fields = ('user__username', 'user__email')
