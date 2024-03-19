from django.urls import path
from . import views
from django.contrib import admin

app_name  = "Users"
urlpatterns = [
     path("Register",views.Registration,name="Registration"),
     path("login",views.Login,name="login"),
     path('testing',views.testing,name='testing'),
     path('',views.index,name='index'),
     path('schedule',views.schedules,name='schedule'),
     path('createTable',views.createTable,name='createTable'),
     path('step_two',views.createTable2,name='step_two'),
     path('chat',views.chatRooms,name='chat'),
     path('Rooms',views.scheduleRooms,name='Rooms'),
     path('Ads',views.advertisement,name='Ads'),
     path('profile',views.profile,name='profile')
    

]