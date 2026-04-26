from django.db import models

# Create your models here. Models are to get information from database
from django.db import models
from django.utils import timezone


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    state = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='devices')
    consumption_per_hour = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.name}"

class DeviceAttribute(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="attributes")
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

class DeviceLogActivation(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="logs")
    state = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.device.name} {self.state} {self.date}"

