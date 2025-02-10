from django.urls import path
from . import views
app_name = 'mastercontrol'

# urlpatterns = [
#     path('master-control/', views.master_control, name='master_control'),
#     path('home/', views.home, name='home'),
# ]
# mastercontrol/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("create_or_join_chatroom/", views.create_or_join_chatroom, name="create_or_join_chatroom"),
    path("chatroom/<str:chatroom_name>/", views.chatroom_detail, name="chatroom_detail"),
    path("allchatrooms/", views.user_chatrooms, name="all_chatrooms"),
]
