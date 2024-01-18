from djongo import models
from django.db import models

# Create your models here.   
class users(models.Model):
    fName = models.CharField(max_length = 100,blank = True)
    lName=  models.CharField(max_length = 100,blank = True)
    userName = models.CharField(max_length = 100,blank = True)
    gender = models.CharField(max_length = 100,blank = True)
    email = models.CharField(max_length = 100,blank = True)
    address = models.CharField(max_length = 100,blank = True)
    address = models.CharField(max_length = 100,blank = True)
    institution = models.CharField(max_length = 100,blank = True)
    picture = models.FileField(blank=True)
    password = models.CharField(max_length = 100,blank = True)
    # passw = models.CharField(max_length = 100,blank = True)

    class Meta:
        db_table = 'user'  # Set the collection name
        app_label = 'Users'  # Set the database names
        
class quotes(models.Model):
    author = models.CharField(max_length=50)
    avatar = models.BinaryField()

