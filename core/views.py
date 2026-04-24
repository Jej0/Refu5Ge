from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Room, Device, DeviceAttribute
from django.db.models import Q

@login_required
def search_rooms(request):
    request.user.profile.points += 1
    request.user.profile.save(update_fields=['points'])
    request.user.profile.check_level_up()

    query = request.GET.get('q', '')
    rooms = Room.objects.all()
    if query:
        rooms = rooms.filter(name__icontains=query)
    return render(request, 'core/search_rooms.html', {'rooms': rooms, 'query': query})

@login_required
def search_devices(request):
    request.user.profile.points += 1
    request.user.profile.save(update_fields=['points'])
    request.user.profile.check_level_up()

    query = request.GET.get('q', '')
    devices = Device.objects.select_related('room').all()
    if query:
        devices = devices.filter(
            Q(name__icontains=query) | Q(type__icontains=query) | Q(room__name__icontains=query)
        )
    return render(request, 'core/search_devices.html', {'devices': devices, 'query': query})

@login_required
def search_attributes(request):
    request.user.profile.points += 1
    request.user.profile.save(update_fields=['points'])
    request.user.profile.check_level_up()

    query = request.GET.get('q', '')
    attributes = DeviceAttribute.objects.select_related('device', 'device__room').all()
    if query:
        attributes = attributes.filter(
            Q(key__icontains=query) | Q(value__icontains=query) | Q(device__name__icontains=query)
        )
    return render(request, 'core/search_attributes.html', {'attributes': attributes, 'query': query})


def home(request):
    return render(request, 'core/home.html')