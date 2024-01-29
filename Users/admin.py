from django.contrib import admin
from .models import *

class TodoAdmin(admin.ModelAdmin):
    list_display = ('')

admin.site.register(users)
admin.site.register(quotes)
admin.site.register(messages)
admin.site.register(chat)
# admin.site.register(trials)

# Register your models here.
