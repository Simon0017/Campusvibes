from django.contrib import admin
from .models import *

class TodoAdmin(admin.ModelAdmin):
    list_display = ('')

# admin.site.register(Users)
# admin.site.register(Quotes)
# admin.site.register(Messages)
# admin.site.register(Chat)
# admin.site.register(trials)

# Register your models here.
