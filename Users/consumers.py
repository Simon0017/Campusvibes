# Users.consumers.py

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from Users.database import *
# from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore
# from django.utils.functional import SimpleLazyObject

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None
        self.user = None
        self.name = None
        self.id = None
        
    def connect(self):
        self.room = self.scope['url_route']['kwargs']['x']

        self.accept()

        
        # join the room
        async_to_sync (self.channel_layer.group_add)(
            self.room,
            self.channel_name
        )


    def disconnect(self,close_code):
        if self.id:
            self.connection.close()

        async_to_sync(self.channel_layer.group_discard)(
            self.room,
            self.channel_name
        )


    def receive(self,text_data = None,byte_data = None):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        userName  = text_data_json.get('username')

        # send the message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.room,{
                'type':'chat_message',
                'message':message,
                'user':userName,
            }
        )

    def chat_message(self,event):
        self.send(text_data=json.dumps(event))

        
    