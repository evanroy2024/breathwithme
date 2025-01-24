"""
URL configuration for breathwme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import routing  # import routing to include WebSocket URLs

urlpatterns = [
    path('', include('mainapp.urls')),  # Replace 'myapp' with your app name\
    path("musicapp/",include('musicapp.urls')),
    path("course/",include('courseapp.urls')),
    path("mastercontrol/",include('mastercontrol.urls')),
    path('admin/', admin.site.urls),
    path("userdetails/",include('userdata.urls')),
    path(r'^ws/', include(routing.websocket_urlpatterns)),  # Include WebSocket URLs

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
