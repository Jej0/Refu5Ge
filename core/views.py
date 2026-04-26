from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Room, Device, DeviceAttribute
from django.db.models import Q

from django.db.models import Q, Count

def search_rooms(request):
    query = request.GET.get('q', '')
    count = request.GET.get('count', '')

    # Points pour utilisateurs connectés
    if request.user.is_authenticated:
        request.user.profile.points += 1
        request.user.profile.save(update_fields=['points'])
        request.user.profile.check_level_up()

    rooms = Room.objects.annotate(num_devices=Count('devices'))

    # Filtre textuel
    if query:
        rooms = rooms.filter(name__icontains=query)

    # Filtre par nombre d'appareils
    if count == 'low':
        rooms = rooms.filter(num_devices__lt=5)
    elif count == 'mid':
        rooms = rooms.filter(num_devices__gte=5, num_devices__lte=10)
    elif count == 'high':
        rooms = rooms.filter(num_devices__gt=10)

    return render(request, 'core/search_rooms.html', {
        'rooms': rooms,
        'query': query,
    })

def search_devices(request):
    query = request.GET.get('q', '')
    piece = request.GET.get('piece', '')      # nouveau filtre
    etat = request.GET.get('etat', '')        # nouveau filtre

    if request.user.is_authenticated:
        request.user.profile.points += 1
        request.user.profile.save(update_fields=['points'])
        request.user.profile.check_level_up()

    devices = Device.objects.select_related('room').all()

    # Filtre texte
    if query:
        devices = devices.filter(
            Q(name__icontains=query) | Q(type__icontains=query) | Q(room__name__icontains=query)
        )
    # Filtre par pièce
    if piece:
        devices = devices.filter(room__id=piece)
    # Filtre par état
    if etat == 'actif':
        devices = devices.filter(state=True)
    elif etat == 'inactif':
        devices = devices.filter(state=False)

    # Liste des pièces pour le menu déroulant
    rooms = Room.objects.all()

    return render(request, 'core/search_devices.html', {
        'devices': devices,
        'query': query,
        'rooms': rooms,
    })
def search_attributes(request):
    query = request.GET.get('q', '')
    device_id = request.GET.get('device', '')

    if request.user.is_authenticated:
        request.user.profile.points += 1
        request.user.profile.save(update_fields=['points'])
        request.user.profile.check_level_up()

    attributes = DeviceAttribute.objects.select_related('device', 'device__room').all()

    if query:
        attributes = attributes.filter(
            Q(key__icontains=query) | Q(value__icontains=query) | Q(device__name__icontains=query)
        )

    if device_id:
        attributes = attributes.filter(device_id=device_id)

    # Récupérer tous les devices pour le menu déroulant
    devices = Device.objects.all()

    return render(request, 'core/search_attributes.html', {
        'attributes': attributes,
        'query': query,
        'devices': devices,
    })
def home(request):
    return render(request, 'core/home.html')
