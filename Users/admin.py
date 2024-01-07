from django.contrib import admin
from .models import *

class TodoAdmin(admin.ModelAdmin):
    list_display = ('')

admin.site.register(users)

# Register your models here.
