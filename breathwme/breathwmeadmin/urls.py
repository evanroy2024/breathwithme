from django.urls import path
from .views import upload_music
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

app_name = 'breathwmeadmin'

urlpatterns = [
    path('upload/', upload_music, name='upload_music'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
