from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.leases.models import Lease
from apps.leases.services import process_renewal_window, send_lease_expiry_reminder


EXPIRY_REMINDER_DAYS = (30, 20, 10, 7, 1)


class Command(BaseCommand):
    help = "Send lease expiry reminders at 30, 20, 10, 7 and 1 day(s)."

    def handle(self, *args, **options):
        today = timezone.localdate()
        initial_window = (
            Lease.objects
            .select_related("tenant", "unit", "unit__property")
            .filter(
                status="active",
                end_date__gte=today,
                end_date__lte=today + timedelta(days=30),
            )
            .order_by("end_date", "lease_number")
        )
        reminder_dates = {
            today + timedelta(days=days): days
            for days in EXPIRY_REMINDER_DAYS[1:]
        }
        subsequent_reminders = (
            Lease.objects
            .select_related("tenant", "unit", "unit__property")
            .filter(
                status="renewal",
                end_date__in=reminder_dates,
            )
            .order_by("end_date", "lease_number")
        )

        eligible = initial_window.count() + subsequent_reminders.count()
        processed = 0
        failed = 0

        for lease in initial_window.iterator():
            try:
                process_renewal_window(lease, window_days=30)
                processed += 1
            except Exception as exc:
                failed += 1
                self.stderr.write(
                    self.style.ERROR(
                        f"Failed to process {lease.lease_number}: {exc}"
                    )
                )

        for lease in subsequent_reminders.iterator():
            try:
                send_lease_expiry_reminder(
                    lease,
                    days_remaining=reminder_dates[lease.end_date],
                )
                processed += 1
            except Exception as exc:
                failed += 1
                self.stderr.write(
                    self.style.ERROR(
                        f"Failed to process {lease.lease_number}: {exc}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Expiry reminder processing complete. "
                f"Eligible: {eligible}; "
                f"processed: {processed}; "
                f"failed: {failed}."
            )
        )
