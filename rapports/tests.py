from datetime import datetime
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from core.models import Device, DeviceLogActivation, Room
from rapports.views import get_monthly_device_report


class MonthlyDeviceReportTests(TestCase):
	def test_day_count_starts_at_midnight_when_device_was_already_on(self):
		room = Room.objects.create(name="Salle 1")
		device = Device.objects.create(
			name="Lampe",
			type="Light",
			description="Lampe du plafond",
			state=False,
			room=room,
			consumption_per_hour=2.0,
		)

		previous_day_on = timezone.make_aware(datetime(2026, 4, 26, 23, 0, 0))
		same_day_off = timezone.make_aware(datetime(2026, 4, 27, 9, 0, 0))
		fixed_now = timezone.make_aware(datetime(2026, 4, 27, 12, 0, 0))

		DeviceLogActivation.objects.create(device=device, state=True, date=previous_day_on)
		DeviceLogActivation.objects.create(device=device, state=False, date=same_day_off)

		with patch("rapports.views.timezone.now", return_value=fixed_now):
			report = get_monthly_device_report(room)

		item = report["items"][0]

		self.assertEqual(item["day_hours"], 9.0)
		self.assertEqual(item["month_hours"], 10.0)
		self.assertEqual(item["day_consumption"], 18.0)
		self.assertEqual(item["month_consumption"], 20.0)
		self.assertEqual(report["total_day_consumption"], 18.0)

