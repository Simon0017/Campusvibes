# # models.py

# from django.db import models
# from djongo import models

# class Users(models.Model):
#     fName = models.CharField(max_length=100, blank=True)
#     lName = models.CharField(max_length=100, blank=True)
#     userName = models.CharField(max_length=100, blank=True)
#     gender = models.CharField(max_length=100, blank=True)
#     email = models.CharField(max_length=100, blank=True)
#     address = models.CharField(max_length=100, blank=True)
#     institution = models.CharField(max_length=100, blank=True)
#     picture = models.ImageField()
#     password = models.CharField(max_length=100, blank=True)

#     def __str__(self):
#         return self.userName


# class Quotes(models.Model):
#     author = models.CharField(max_length=50)
#     avatar = models.ImageField()
#     quotation = models.TextField(null=True)

#     def __str__(self):
#         return self.author


# class Chat(models.Model):
#     participants = models.JSONField()


# class Messages(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     sender = models.ForeignKey(Users, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
