from django.urls import path
from .views import upload_userdata ,update_setting

app_name = 'userdata'


urlpatterns = [
    path("upload-userdata/", upload_userdata, name="upload_userdata"),
    path('update-setting/', update_setting, name='update-setting'),
]
