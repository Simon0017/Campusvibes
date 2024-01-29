from django.db import models
from djongo import models


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
    picture = models.ImageField()
    password = models.CharField(max_length = 100,blank = True)
 
    def __str__(self):
        return self.userName
    
        
class quotes(models.Model):
    author = models.CharField(max_length=50)
    avatar = models.ImageField()
    quotation = models.TextField(null = True)

    def __str__(self):
        return self.author
    
class chat(models.Model):
    participants = models.ArrayReferenceField(to=users, on_delete=models.CASCADE)
    # participants = models.ArrayField(models.IntegerField(), default=list)


class messages(models.Model):
    chat = models.ForeignKey(chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(users, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


