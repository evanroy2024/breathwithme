from django.contrib import admin
from .models import Userdata
admin.site.register(Userdata)



from django.contrib import admin
from .models import HabitPreference

@admin.register(HabitPreference)
class HabitPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'practice_frequency', 'preferred_time', 'allow_notifications', 'goal')
    list_filter = ('experience', 'practice_frequency', 'preferred_time', 'goal')
