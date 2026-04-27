import csv
from datetime import timedelta
from typing import TypedDict

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.utils import timezone
from core.models import Room, Device, DeviceLogActivation


class MonthlyReportItem(TypedDict):
    device: Device
    activation_count: int
    month_hours: float
    day_hours: float
    consumption_per_hour: float
    day_consumption: float
    month_consumption: float


class MonthlyReport(TypedDict):
    items: list[MonthlyReportItem]
    total_day_consumption: float
    total_month_consumption: float


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
    
    for item in monthly_report["items"]:
        device = item["device"]

        writer.writerow([
            room.name,
            device.name,
            "Allumé" if device.state else "Éteint",
            item["activation_count"],
            item["month_hours"],
            item["consumption_per_hour"],
            item["month_consumption"],
        ])

    return response


def _compute_active_time(device, logs, start, end) -> tuple[timedelta, int]:
    active_time = timedelta()
    activation_count = 0

    previous_log = device.logs.filter(date__lt=start).order_by("-date").first()
    current_state = bool(previous_log.state) if previous_log else False
    active_since = start if current_state else None

    for log in logs:
        if log.state == current_state:
            continue

        if log.state:
            current_state = True
            activation_count += 1
            active_since = log.date
        else:
            if active_since is not None:
                active_time += log.date - active_since
            current_state = False
            active_since = None

    if current_state and active_since is not None:
        active_time += end - active_since

    return active_time, activation_count


def get_monthly_device_report(room) -> MonthlyReport:
    now = timezone.now()
    start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    report_items: list[MonthlyReportItem] = []

    total_day_consumption = 0
    total_month_consumption = 0

    devices = room.devices.all().prefetch_related("logs")

    for device in devices:
        logs_month = device.logs.filter(date__gte=start_month).order_by("date")
        logs_day = device.logs.filter(date__gte=start_day).order_by("date")

        total_month_active_time, activation_count = _compute_active_time(
            device,
            logs_month,
            start_month,
            now,
        )
        total_day_active_time, _ = _compute_active_time(
            device,
            logs_day,
            start_day,
            now,
        )

        month_hours = round(total_month_active_time.total_seconds() / 3600, 2)
        day_hours = round(total_day_active_time.total_seconds() / 3600, 2)

        consumption_per_hour = device.consumption_per_hour or 0

        month_consumption = round(month_hours * consumption_per_hour, 2)
        day_consumption = round(day_hours * consumption_per_hour, 2)

        total_month_consumption += month_consumption
        total_day_consumption += day_consumption

        report_items.append({
            "device": device,
            "activation_count": activation_count,
            "month_hours": month_hours,
            "day_hours": day_hours,
            "consumption_per_hour": consumption_per_hour,
            "day_consumption": day_consumption,
            "month_consumption": month_consumption,
        })

    return {
        "items": report_items,
        "total_day_consumption": round(total_day_consumption, 2),
        "total_month_consumption": round(total_month_consumption, 2),
    }
