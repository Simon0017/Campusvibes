# Users.consumers.py

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from Users.database import *
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore
from django.utils.functional import SimpleLazyObject

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None
        self.user = None
        
    def connect(self):
        session_key = self.scope.get("session").session_key

        # Create a session store using the session key
        session_store = SessionStore(session_key=session_key)

        # Get the user_id from the session
        self.id = session_store.get('user_id')

        #retrieve the rooms the user is and the username
        self.rooms = chats.objects.get(reference_id = self.id).all()
        self.name = session_store.get('username') 
        
        # get room data
        
        self.accept()
         # send the user list to the  user
        self.send(json.dumps({
            'type': 'user_list',
            'users': [user for user in self.rooms.contacts],
        }))

        
    