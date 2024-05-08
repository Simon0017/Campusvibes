'''
This is to replace the model.py file.No migrations necessary
'''

from mongoengine import *

conn = connect('Campusvibes_v2')

class user_data(Document):
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    user_name = StringField(max_length=50)
    gender = StringField(max_length=10)
    email = EmailField()
    address  =StringField(max_length=50)
    institution = StringField(max_length=100)
    # picture  = ImageField()
    password = StringField(max_length=500)
    time_registered = DateTimeField()
    contacts = ListField(StringField())
    rooms = ListField(StringField())

class quotes(Document):
    avatar = ImageField()
    author = StringField(max_length=50)
    text = StringField()

class chats(Document):
    reference_id = StringField(max_length=250)
    reference_contact = StringField(max_length=250)
    contacts = ListField(StringField(max_length=250))
    time_created = DateTimeField()

class messages(DynamicDocument):
    chat_id = StringField(max_length=250)
    sender = StringField(max_length=50)
    message = DynamicField()
    timestamp = DateTimeField()

class rooms(Document):
    name = StringField()
    Type = StringField()
    room_description = StringField()
    administrators = ListField(StringField(max_length=50))
    members =ListField(StringField(max_length=100))
    password = StringField(max_length=200)
    date_created = DateTimeField()
    no_of_time_div = IntField()
    format = StringField()


class timetables(Document):
    room_id = StringField()
    room_name = StringField()
    table = ListField(ListField())
    timestamp = DateTimeField()

class resources(Document):
    room_id = ReferenceField(rooms)
    category = StringField()
    file = FileField()
    text = StringField()
    timestamp = DateTimeField()




