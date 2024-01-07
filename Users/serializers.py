# serializers are responsible for converting model instances into JSON helping
# the frontend to work with the data easily

from rest_framework import serializers
from .models import *

class userSerializers(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ('id','fname','lname','userName','gender','email','address',
                  'institution','picture','password','passw')