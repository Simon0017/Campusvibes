from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password,check_password
import pymongo as py
from bson import json_util,ObjectId
import datetime
from mongoengine import *
from Users.database import *
from django.contrib.sessions.models import Session
import datetime


# connecting to the connection string and the db
# conn = py.MongoClient("mongodb://localhost:27017/")
# db = conn['Campusvibes_v2']

# view handling the registration page
def Registration(request):
    if request.method =='POST':
        # creating an instance of the class
        user_info = user_data()

        # extracting the data and saaving them in the db
        user_info.first_name = request.POST.get('FirstName')
        user_info.last_name = request.POST.get('LastName')
        user_info.user_name = request.POST.get('Username')
        user_info.gender = request.POST.get('gender')
        user_info.email = request.POST.get('email')
        user_info.address = request.POST.get('address')
        user_info.institution = request.POST.get('institution')
        user_info.time_registered = datetime.datetime.now()
        # picture = request.POST.get('picture')
        password = request.POST.get('password')
        user_info.password= make_password(password)
        passw = request.POST.get('passw')

        # check if the passwords match before inserting the data
        if (password==passw):
            user_info.save()
            return redirect("Users:Registration")
        else:
            return HttpResponse('Please provide matching passwords')
    
    return render(request,"Users/userRegistration.html")


# view handling the login page

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('passw')
        
        # Query the user_data collection for the username
        user = user_data.objects(user_name=username).first()

        if user and check_password(password, user.password):
            # Authentication successful, set session variables
            request.session['username'] = user.user_name
            request.session['user_id'] = str(user.pk)
            print(request.session.get('username'))
            return redirect('Users:index')
        else:
            return HttpResponse('Username or Password incorrect')

    return render(request, "Users/login.html")



# redundant view for the base template for all pages
def testing(request):
    return render(request,'Users/testingNav.html')


# view for the home page
def index(request):
    return render(request,'Users/indexMain.html')

# view for manage schedules
def schedules(request):
    if request.method =='POST':
        # instance of the classes
        room_data = rooms()

        room_data.name = request.POST.get('room_name')
        room_data.Type = request.POST.get('room_type')
        room_data.room_description = request.POST.get('description')

        # save and redirection
        if room_data.save():
            '''
            here the program retrieves the data already submitted of the immediately created room 
            and created a session of the room id which is destroyed immeadiately after the room details are 
            updated
            '''
            room_retrv = rooms.objects(name=room_data.name).first()
            request.session['room_id'] = str(room_retrv.pk)
            return redirect('Users:createTable')
        else:
            return HttpResponse('Something went wrong pleae try again')
        
    return render(request,'Users/Schedules.html')

# view on the second stage of creating the table
def createTable(request):
    if request.method =='POST':
        # create instance of the class
        update = rooms()

        # retrieve room data with the session created in the schedules view
        data = rooms.objects(pk=request.session['room_id']).first()
        data.format = request.POST.get('format')
        data.administrators.append(request.session['username'])
        data.members.append(request.session['username'])
        data.no_of_time_div =request.POST.get('periods')

        # get the user_data to save in the userdata.room field
        user = user_data.objects(user_name = request.session['username']).first()
        user.rooms.append(request.session['room_id'])

        # save the update
        if data.save() and user.save():
            return redirect('Users:step_two')
        else:
            return HttpResponse('Something went wrong please try again')
        
    return render(request,'Users/tableCreation.html')


# view for step two of table creation
def createTable2(request):
    # retrieve the data of the room
    data = rooms.objects(pk=request.session['room_id']).first()
    # create an empty list and add zeros to create a necceasry list for the template to loop through
    my_list = []
    for x in range(data.no_of_time_div):
        my_list.append(0)
    
    context = {
        "Range":my_list
    }
    if request.method=='POST':
        # creating arrays as we are going to store data in arrays
        periods = []
        monday = []
        tuesday =[]
        wednesday = []
        thursday = []
        friday = []
        saturday = []
        for j in range(data.no_of_time_div):
            periods.append(request.POST.get(f'period{j}'))
            monday.append(request.POST.get(f'm{j}'))
            tuesday.append(request.POST.get(f'tu{j}'))
            wednesday.append(request.POST.get(f'w{j}'))
            thursday.append(request.POST.get(f'th{j}'))
            friday.append(request.POST.get(f'f{j}'))
            saturday.append(request.POST.get(f's{j}'))
        # retrieve room id and name
        data = rooms.objects(pk=request.session['room_id']).first()
        room_name = data.name

        # create an instance of class inorder to save the file
        table = timetables()
        table.room_id = request.session['room_id']
        table.room_name  = room_name
        table.table.append(periods)
        table.table.append(monday)
        table.table.append(tuesday)
        table.table.append(wednesday)
        table.table.append(thursday)
        table.table.append(friday)
        table.table.append(saturday)

        if table.save():
            # try:
            #     from django.utils import timezone
            #     session = Session.objects.get(session_key='room_id')
            #     # Optionally, you can check if the session is expired before deleting
            #     if session.expire_date < timezone.now():
            #         session.delete()
            #     else:
            #         print('Session already expired') # Session is already expired
            # except Session.DoesNotExist:
            #     print('Session doe not exist') # Session with given session key doesn't exist
            # # session = request.session['room_id']
            # # session.delete()
            return redirect('Users:index') #save and reidrect back to the home page
        else:
            return HttpResponse('Try again.Something went wrong')


    return render(request,'Users/table_step2.html',context)


# view for the chat room
def chatRooms(request):
    if request.method == 'POST':
        query = request.POST.get('contacts')
        user_id = request.session['user_id']
        
        # Check if a chat object already exists for the given user and contacts
        chat = chats.objects.filter(reference_id=user_id, contacts=query).first()
        
        # If chat object does not exist, create a new one
        if not chat:
            chat = chats(reference_id=user_id, contacts=query, time_created=datetime.datetime.now())
            chat.save()
        
        context = {
            'contact': chat
        }
        return render(request, 'Users/chatRoom.html', context)
    return render(request, 'Users/chatRoom.html')


# view for the spaces /rooms interface
def scheduleRooms(request):
    # checking the rooms in which the session ID is participating 
    username = request.session['username']

    # Fetch all rooms ID in which the user is in from the user_data.rooms
    room_ID = user_data.objects(user_name = username).values_list('rooms').first()
    
    # Initialize variables
    public_data = []
    private_data = []
    timetable_public = []
    timetable_private = []
    pub_data = []
    priv_data = []
    day = datetime.datetime.now().strftime('%A')
    pub_time = []
    priv_time = []
    namePub = []
    namePriv = []

    for id in room_ID:
        room = rooms.objects(pk = id).first()
        if room.Type =='public':
            table = timetables.objects(room_id = id).first()
            # saving the data in list initialized aboce for the public instance
            public_data.append(room)
            timetable_public.append(table.table)
            namePub.append(room.name)

            # for the day data
            if day == 'Monday':
                pub_data.append(table.table[1])
            elif day =='Tuesday':
                pub_data.append(table.table[2])
            elif day =='Wednesday':
                pub_data.append(table.table[3])
            elif day =='Thursday':
                pub_data.append(table.table[4])
            elif day =='Friday':
                pub_data.append(table.table[5])
            elif day =='Saturday':
                pub_data.append(table.table[6])
            else:
                pub_data.append(table.table[1])

            pub_time.append(table.table[0])

        elif room.Type =='private':
            table_priv =timetables.objects(room_id = id).first()
            # saving the data for the private instance
            private_data.append(room)
            timetable_private.append(table_priv.table)
            namePriv.append(room.name)

            # for the day data
            if day == 'Monday':
                priv_data.append(table_priv.table[1])
            elif day =='Tuesday':
                priv_data.append(table_priv.table[2])
            elif day =='Wednesday':
                priv_data.append(table_priv.table[3])
            elif day =='Thurday':
                priv_data.append(table_priv.table[4])
            elif day =='Friday':
                priv_data.append(table_priv.table[5])
            elif day =='Saturday':
                priv_data.append(table_priv.table[6])
            else:
                priv_data.append(table_priv.table[1])

            priv_time.append(table_priv.table[0])
    
     # Combine todayPub and timePub into a list of tuples
    today_pub_combined = list(zip(pub_data, pub_time,namePub))

    # Combine todayPriv and timePriv into a list of tuples
    today_priv_combined = list(zip(priv_data, priv_time,namePriv))

     
    context = {
        'today':day,
        'timetable_pub':timetable_public,
        'timetable_priv':timetable_private,
        'roomPriv':private_data,
        'roomPub':public_data,
        'todayPub':pub_data,
        'todayPriv':priv_data,
        'todayPubCombined': today_pub_combined,
        'todayPrivCombined': today_priv_combined,
        'namepub':namePub,
        'namepriv':namePriv,
    }

    return render(request,'Users/scheduleRooms.html',context)

# view for advertisement
def advertisement(request):
    return render(request,'Users/advertisement.html')


# view for the profile page

def profile(request):
    user_name = request.session['username']
    user = user_data.objects(user_name=user_name).first()
    context ={
        'data':user
    }
    return render(request,'Users/userProfile.html',context)

# view for the space panel
def space(request,space):
    table_data = timetables.objects(room_name = space).first()
    table= table_data.table

    periods = [x for x in table[0]]
    monday = [x for x in table[1]]
    tues = [x for x in table[2]]
    wed = [x for x in table[3]]
    thurs = [x for x in table[4]]
    fri = [x for x in table[5]]
    sat = [x for x in table[6]]

    timetable1 = list(zip(periods,monday,tues,wed,thurs,fri,sat))

    context = {
        'name':space,
        'table':table,
        'tableData':table_data,
        'ranges':periods,
        'timetable':timetable1,
    }
    return render(request,'Users/space.html',context)

# Create your views here.
