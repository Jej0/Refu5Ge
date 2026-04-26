from datetime import timedelta
from django.utils import timezone
import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from core.models import Room, Device, DeviceAttribute, DeviceLogActivation


def rapports_accueil(request):
    rooms = Room.objects.annotate(nombre_objets=Count("devices"))

    total_rooms = Room.objects.count()
    total_devices = Device.objects.count()
    active_devices = Device.objects.filter(state=True).count()
    inactive_devices = Device.objects.filter(state=False).count()
    total_logs = DeviceLogActivation.objects.count()

    context = {
        "rooms": rooms,
        "total_rooms": total_rooms,
        "total_devices": total_devices,
        "active_devices": active_devices,
        "inactive_devices": inactive_devices,
        "total_logs": total_logs,
    }

    return render(request, "rapports/accueil.html", context)


def rapport_global(request):
    total_rooms = Room.objects.count()
    total_devices = Device.objects.count()
    active_devices = Device.objects.filter(state=True).count()
    inactive_devices = Device.objects.filter(state=False).count()
    total_logs = DeviceLogActivation.objects.count()

    room_most_devices = (
        Room.objects
        .annotate(nombre_objets=Count("devices"))
        .order_by("-nombre_objets")
        .first()
    )

    recent_logs = (
        DeviceLogActivation.objects
        .select_related("device", "device__room")
        .order_by("-date")[:10]
    )

    context = {
        "total_rooms": total_rooms,
        "total_devices": total_devices,
        "active_devices": active_devices,
        "inactive_devices": inactive_devices,
        "total_logs": total_logs,
        "room_most_devices": room_most_devices,
        "recent_logs": recent_logs,
    }

    return render(request, "rapports/global.html", context)


def rapport_piece(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    devices = (
        Device.objects
        .filter(room=room)
        .prefetch_related("attributes", "logs")
    )

    total_devices = devices.count()
    active_devices = devices.filter(state=True).count()
    inactive_devices = devices.filter(state=False).count()

    device_stats = []

    for device in devices:
        logs_count = device.logs.count()
        attributes = device.attributes.all()

        if not device.state:
            observation = "Objet inactif : vérification possible."
        elif logs_count == 0:
            observation = "Aucun historique : données insuffisantes."
        else:
            observation = "Fonctionnement normal."

        device_stats.append({
            "device": device,
            "logs_count": logs_count,
            "attributes": attributes,
            "observation": observation,
        })

    context = {
        "room": room,
        "devices": devices,
        "total_devices": total_devices,
        "active_devices": active_devices,
        "inactive_devices": inactive_devices,
        "device_stats": device_stats,
    }

    return render(request, "rapports/piece.html", context)


def historique(request):
    logs = (
        DeviceLogActivation.objects
        .select_related("device", "device__room")
        .order_by("-date")
    )

    context = {
        "logs": logs,
    }

    return render(request, "rapports/historique.html", context)


def maintenance(request):
    devices = Device.objects.prefetch_related("logs", "attributes").select_related("room")

    objets_a_surveiller = []

    for device in devices:
        logs_count = device.logs.count()
        attributes_count = device.attributes.count()

        raison = None

        if not device.state:
            raison = "Objet inactif : maintenance ou vérification nécessaire."
        elif logs_count == 0:
            raison = "Aucun historique d’activation disponible."
        elif attributes_count == 0:
            raison = "Aucun attribut renseigné pour cet objet."

        if raison:
            objets_a_surveiller.append({
                "device": device,
                "room": device.room,
                "logs_count": logs_count,
                "attributes_count": attributes_count,
                "raison": raison,
            })

    context = {
        "objets_a_surveiller": objets_a_surveiller,
    }

    return render(request, "rapports/maintenance.html", context)

def export_room_csv(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    monthly_report = get_monthly_device_report(room)

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="rapport_{room.name}.csv"'

    writer = csv.writer(response)

    writer.writerow([
        "Pièce",
        "Device",
        "État actuel",
        "Nombre d'activations ce mois",
        "Temps total allumé ce mois (heures)",
        "Consommation par heure (kWh/h)",
        "Consommation estimée du mois (kWh)",
    ])

    for item in monthly_report:
        device = item["device"]

        writer.writerow([
            room.name,
            device.name,
            "Allumé" if device.state else "Éteint",
            item["activation_count"],
            item["total_hours"],
            item["consumption_per_hour"],
            item["monthly_consumption"],
        ])

    return response

def get_monthly_device_report(room):
    now = timezone.now()
    start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    report = []

    devices = room.devices.all().prefetch_related("logs")

    for device in devices:
        logs = device.logs.filter(date__gte=start_month).order_by("date")

        total_active_time = timedelta()
        activation_start = None
        activation_count = 0

        for log in logs:
            if log.state is True:
                activation_start = log.date
                activation_count += 1
            elif log.state is False and activation_start is not None:
                total_active_time += log.date - activation_start
                activation_start = None

        if activation_start is not None:
            total_active_time += now - activation_start

        total_hours = round(total_active_time.total_seconds() / 3600, 2)
        monthly_consumption = round(total_hours * device.consumption_per_hour, 2)

        report.append({
            "device": device,
            "activation_count": activation_count,
            "total_hours": total_hours,
            "consumption_per_hour": device.consumption_per_hour,
            "monthly_consumption": monthly_consumption,
        })

    return report
