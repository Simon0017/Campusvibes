from django.urls import path
from . import views
from django.contrib import admin

app_name  = "Users"
urlpatterns = [
     path("Register",views.Registration,name="Registration"),
     path("login",views.Login,name="login"),
     path('testing',views.testing,name='testing'),
     path('index',views.index,name='index'),
     path('schedule',views.schedules,name='schedule'),
     path('createTable',views.createTable,name='createTable'),
    

]