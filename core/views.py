from datetime import date

from django.shortcuts import redirect, render, get_object_or_404
from django.apps import apps

# Create your views here.
from django.views.generic import ListView, UpdateView, DetailView
from .models import *
from .forms import *

def home(request):
    return render(request, 'core/home.html')


from django.shortcuts import render
from django.db.models import Q
from .models import Room, Device, DeviceAttribute

def search_rooms(request):
    query = request.GET.get('q', '')
    rooms = Room.objects.all()
    if query:
        rooms = rooms.filter(name__icontains=query)
    return render(request, 'core/search_rooms.html', {
        'rooms': rooms,
        'query': query
    })

def search_devices(request):
    query = request.GET.get('q', '')
    devices = Device.objects.select_related('room').all()
    if query:
        devices = devices.filter(
            Q(name__icontains=query) | Q(type__icontains=query) | Q(room__name__icontains=query)
        )
    return render(request, 'core/search_devices.html', {
        'devices': devices,
        'query': query
    })

def search_attributes(request):
    query = request.GET.get('q', '')
    attributes = DeviceAttribute.objects.select_related('device', 'device__room').all()
    if query:
        attributes = attributes.filter(
            Q(key__icontains=query) | Q(value__icontains=query) | Q(device__name__icontains=query)
        )
    return render(request, 'core/search_attributes.html', {
        'attributes': attributes,
        'query': query
    })