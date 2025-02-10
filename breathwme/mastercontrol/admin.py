from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ChatRoom , Member
# Register your models here.


admin.site.register(ChatRoom)

admin.site.register(Member)
