from django.urls import path
from .views import upload_userdata

app_name = 'userdata'


urlpatterns = [
    path("upload-userdata/", upload_userdata, name="upload_userdata"),
]
