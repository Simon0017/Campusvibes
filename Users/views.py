from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password,check_password
import pymongo as py
from bson import json_util

# connecting to the connection string and the db
conn = py.MongoClient("mongodb://localhost:27017/")
db = conn['Campusvibes']

# view handling the registration page
def Registration(request):
    if request.method =='POST':
        fname = request.POST.get('FirstName')
        lname = request.POST.get('LastName')
        userName = request.POST.get('Username')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        address = request.POST.get('address')
        instituiton = request.POST.get('institution')
        picture = request.POST.get('picture')
        password = request.POST.get('password')
        hashedPassword = make_password(password)
        passw = request.POST.get('passw')

        # specifying the collection name
        coll = db['users']

        # check if the passwords match before inserting the data
        if (password==passw):
            coll.insert_one({'first_name':fname,
                            'last_name':lname,
                             'username':userName,
                              'gender':gender,
                               'email':email,
                                'address':address,
                                 'institution':instituiton,
                                  'password':hashedPassword})
            return redirect("Users:Registration")
    
    return render(request,"Users/userRegistration.html")


# view handling the login page
def Login(request):
    if request.method =='POST':
        userName = request.POST.get('Username')
        password = request.POST.get('passw')
        # return render(request,"Users/registrationUsers.html")
         
        # specifying the collection name
        coll = db['users']

        username = coll.find_one({'username':userName})
        is_passw_valid = check_password(password,username['password'])

        if username and is_passw_valid:
            return render(request,"Users/indexMain.html")
        else:
            return HttpResponse('Username or Password incorrect')


    return render(request,"Users/login.html")


def testing(request):
    return render(request,'Users/testingNav.html')

def index(request):
    return render(request,'Users/indexMain.html')

def schedules(request):
    return render(request,'Users/Schedules.html')

def createTable(request):
    return render(request,'Users/tableCreation.html')

def createTable2(request):
    return render(request,'Users/table_step2.html')

def chatRooms(request):
    return render(request,'Users/chatRoom.html')

def scheduleRooms(request):
    return render(request,'Users/scheduleRooms.html')

def advertisement(request):
    return render(request,'Users/advertisement.html')

# Create your views here.
