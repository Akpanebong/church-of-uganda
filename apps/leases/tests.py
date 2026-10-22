from datetime import date, timedelta
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from apps.leases.models import Lease
from apps.properties.models import Property, Unit
from apps.tenants.models import Tenant


class LeaseExpiryNotificationCommandTests(TestCase):
    def setUp(self):
        property_ = Property.objects.create(
            code="PROP-TEST",
            name="Test property",
            property_type="residential",
            address="Test address",
        )
        unit = Unit.objects.create(property=property_, unit_number="1A")
        tenant = Tenant.objects.create(
            tenant_id="TEN-TEST",
            full_name="Test tenant",
            phone="0000000000",
        )
        self.today = date(2026, 1, 1)

        for index, days in enumerate((30, 20, 10, 7, 1, 2, 31)):
            Lease.objects.create(
                lease_number=f"LEASE-{index}",
                tenant=tenant,
                unit=unit,
                start_date=self.today - timedelta(days=365),
                end_date=self.today + timedelta(days=days),
                rent=100,
                status="renewal" if days in (20, 10, 7, 1) else "active",
            )

    @patch("apps.leases.management.commands.send_lease_expiry_notifications.send_lease_expiry_reminder")
    @patch("apps.leases.management.commands.send_lease_expiry_notifications.timezone.localdate")
    def test_processes_only_configured_milestones(self, localdate, send_reminder):
        localdate.return_value = self.today

        call_command("send_lease_expiry_notifications")

        self.assertEqual(send_reminder.call_count, 4)
        days_sent = sorted(call.kwargs["days_remaining"] for call in send_reminder.call_args_list)
        self.assertEqual(days_sent, [1, 7, 10, 20])
