from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password,check_password

def Registration(request):
    if request.method =='POST':
        fname = request.POST.get('FirstName')
        lname = request.POST.get('Lastname')
        userName = request.POST.get('Username')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        address = request.POST.get('address')
        instituiton = request.POST.get('institution')
        picture = request.POST.get('picture')
        password = request.POST.get('password')
        hashedPassword = make_password(password)
        passw = request.POST.get('passw')
        # check if the passwords match before inserting the data
        if (password==passw):
            users.objects.create(fName = fname,lName = lname,userName = userName,gender = gender,
                                email = email,address = address,institution = instituiton,picture =picture,
                                password = hashedPassword)
            return redirect("Users:Registration")
    
    return render(request,"Users/userRegistration.html")


def Login(request):
    if request=='POST':
        userName = request.POST.get('Username')
        password = request.POST.get('passw')

        username = users.objects.get(userName=username)
        is_passw_valid = check_password(userName,userName.passsword)

        if (is_passw_valid==True):
            return render(request,"Users/registrationUsers.html")


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

# Create your views here.
