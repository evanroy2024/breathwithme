from django.urls import re_path
from mastercontrol.consumers import ChatConsumer  # Import consumer from the app

websocket_urlpatterns = [
    re_path(r'ws/chatroom/(?P<chatroom_name>\w+)/$', ChatConsumer.as_asgi()),  # WebSocket routing
]
