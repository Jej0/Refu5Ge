from django.contrib import admin
from .models import Room, Device, DeviceAttribute

admin.site.register(Room)
admin.site.register(Device)
admin.site.register(DeviceAttribute)