# routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/Users/chat_room/(?P<x>\w+)/$', consumers.ChatConsumer.as_asgi()),
]