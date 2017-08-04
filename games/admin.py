from django.contrib import admin

from .models import GomokuOnline, Room, Chat, Message

# Register your models here.

admin.site.register(GomokuOnline)
admin.site.register(Room)
admin.site.register(Chat)
admin.site.register(Message)
