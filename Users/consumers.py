# Users.consumers.py

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from Users.database import *
# from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore
# from django.utils.functional import SimpleLazyObject
import datetime

# consumer for individual chat
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

        #retrieve data of the room
        query = messages.objects(chat_id = self.room).order_by('timestamp')

        # side function to split time and get date and also the hr:min
        def timeSplitter(timestamp):
            date= timestamp.date()
            tail  = ''
            hr = timestamp.time().hour
            if hr >=12:
                hr -=12
                tail = 'PM'
            else:
                tail = 'AM'
            
            minute = timestamp.time().minute
            if minute < 10:
                minute = f'0{minute}'
            time = f'{hr}:{minute} {tail}'

            return time
        
        # send chat history
        self.send(json.dumps({
            'type': 'chat_history',
            'message': [{'user': message.sender,
                         'content': message.message,
                         'timestamp':timeSplitter(message.timestamp)} for message in query]
        }))


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

        # save to mongodb database
        message_data = messages(chat_id = self.room,sender = userName,
                                message = message,timestamp = datetime.datetime.now())
        message_data.save()

    def chat_message(self,event):
        self.send(text_data=json.dumps(event))


# consumer for the groupchat on space.html
class RoomGroupChat(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = None

    def connect(self):
        self.room = self.scope['url_route']['kwargs']['space']

        self.accept()

        
        # join the room
        async_to_sync (self.channel_layer.group_add)(
            self.room,
            self.channel_name
        )

        #retrieve data of the room
        query = messages.objects(chat_id = self.room).order_by('timestamp')

        # side function to split time and get date and also the hr:min
        def timeSplitter(timestamp):
            date= timestamp.date()
            tail  = ''
            hr = timestamp.time().hour
            if hr >=12:
                hr -=12
                tail = 'PM'
            else:
                tail = 'AM'
            
            minute = timestamp.time().minute
            if minute < 10:
                minute = f'0{minute}'
            time = f'{hr}:{minute} {tail}'

            return time
        
        # send chat history
        self.send(json.dumps({
            'type': 'chat_history',
            'message': [{'user': message.sender,
                         'content': message.message,
                         'timestamp':timeSplitter(message.timestamp)} for message in query]
        }))


    def disconnect(self,close_code):

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
                'type':'groupMessage',
                'message':message,
                'user':userName,
            }
        )

        # save to mongodb database
        message_data = messages(chat_id = self.room,sender = userName,
                                message = message,timestamp = datetime.datetime.now())
        message_data.save()

    def groupMessage(self,event):
        self.send(text_data=json.dumps(event))

