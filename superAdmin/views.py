from django.shortcuts import render
from django.core.mail import EmailMessage
from django.shortcuts import redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password,check_password
import pymongo as py
from bson import json_util,ObjectId
import datetime
from mongoengine import *
from Users.database import *
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.urls import reverse

# Create your views here.

# view for the index
def index(request):
    return render(request,'index.html')


# view for the base template
def base(request):
    return render(request,'base.html')