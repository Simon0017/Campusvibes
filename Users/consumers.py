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

        session_key = self.scope.get("session").session_key

        # Create a session store using the session key
        session_store = SessionStore(session_key=session_key)

        # Get the user_id and username from the session
        self.id = session_store.get('user_id')
        self.name = session_store.get('username')
        # print(self.name)

        # retreive the username from the db
        self.user = user_data.objects(user_name = self.name).values_list("user_name").first()

        self.accept()

        # session_key = self.scope['session'].session_key
        # Session= SessionStore(session_key)
        # my_variable = Session.get('username')
        # print(my_variable)
        
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
        print(userName)

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

        
    