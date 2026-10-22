from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta

from apps.core.models import Notification
from apps.core.utils import generate_reference
from apps.finance.models import Invoice
from apps.tenants.models import TenantUnit, Tenant


def get_invoice_status(paid_amount, amount):
    """Determine invoice status from the amount paid and total amount due."""
    paid_amount = Decimal(str(paid_amount or 0))
    amount = Decimal(str(amount or 0))

    if paid_amount <= 0:
        return "unpaid"
    if paid_amount >= amount:
        return "paid"
    return "partial"


@transaction.atomic
def sync_lease(instance):
    """Keep the tenancy, unit, tenant and rent invoice aligned with the lease."""
    today = timezone.localdate()
    renewal_window = today <= instance.end_date <= today + timedelta(days=30)
    if instance.status == "active" and renewal_window:
        process_renewal_window(instance)

    is_occupied = instance.status in {"active", "renewal"}

    # Synchronize unit availability.
    other_occupied = instance.unit.leases.exclude(pk=instance.pk).filter(status__in=["active", "renewal"]).exists()
    instance.unit.status = "occupied" if is_occupied or other_occupied else "available"
    instance.unit.save(update_fields=["status", "updated_at"])

    # Synchronize the tenant-unit relationship and tenant status.
    if is_occupied:
        TenantUnit.objects.update_or_create(
            tenant=instance.tenant,
            unit=instance.unit,
            defaults={
                "move_in": instance.start_date,
                "move_out": instance.end_date,
                "active": True,
            },
        )

        if instance.tenant.status != "active":
            instance.tenant.status = "active"
            instance.tenant.save(update_fields=["status", "updated_at"])

    # Calculate the invoice amounts and status.
    amount = instance.rent + instance.service_charge
    paid_amount = instance.deposit
    invoice_status = get_invoice_status(paid_amount, amount)

    # Create or retrieve the invoice for this lease.
    invoice, created = Invoice.objects.get_or_create(
        lease=instance,
        defaults={
            "invoice_number": generate_reference(
                "INV", Invoice, "invoice_number"
            ),
            "tenant": instance.tenant,
            "unit": instance.unit,
            "issue_date": timezone.localdate(),
            "due_date": instance.start_date,
            "description": f"Rent and service charge for {instance.unit}",
            "amount": amount,
            "paid_amount": paid_amount,
            "status": invoice_status,
        },
    )

    # Keep existing invoices synchronized with the lease.
    if not created:
        invoice.tenant = instance.tenant
        invoice.unit = instance.unit
        invoice.due_date = instance.start_date
        invoice.description = (
            f"Rent and service charge for {instance.unit}"
        )
        invoice.amount = amount
        invoice_status = get_invoice_status(invoice.paid_amount, amount)
        invoice.status = invoice_status

        invoice.save(
            update_fields=[
                "tenant",
                "unit",
                "due_date",
                "description",
                "amount",
                "paid_amount",
                "status",
                "updated_at",
            ]
        )

    return invoice


# def send_renewal_notice(instance, user=None):
#     """Send one renewal notice and move an active lease into renewal pending."""
#     if instance.status != "active":
#         return False
#     if instance.tenant.email and not instance.expiry_notice_sent:
#         send_mail(
#             subject=f"Lease renewal notice: {instance.lease_number}",
#             message=(f"Dear {instance.tenant.full_name},\n\nYour lease {instance.lease_number} for "
#                      f"{instance.unit.property.name}, unit {instance.unit.unit_number}, expires on "
#                      f"{instance.end_date:%d %B %Y}. Please contact the Diocesan Estates Department "
#                      "to discuss renewal arrangements.\n\nRegards,\nDiocesan Estates Department"),
#             from_email=None,
#             recipient_list=[instance.tenant.email],
#             fail_silently=False,
#         )
#         instance.expiry_notice_sent = True
#     instance.status = "renewal"
#     fields = ["status"]
#     if instance.expiry_notice_sent:
#         fields.append("expiry_notice_sent")
#         if user and user.is_authenticated:
#             Notification.objects.create(
#                 user=user,
#                 title=f"Lease renewal notice: {instance.lease_number}",
#                 message=(f"Your lease {instance.lease_number} for "
#                          f"{instance.unit.property.name}, unit {instance.unit.unit_number}, expires on "
#                          f"{instance.end_date:%d %B %Y}. An email notification has been sent to {instance.tenant.full_name} "
#                          f"({instance.tenant.email}) "
#                          "to discuss renewal arrangements.")
#             )
#     instance.save(update_fields=fields + ["updated_at"])
#     return True


# def process_renewal_window(instance):
#     today = timezone.localdate()
#     if today <= instance.end_date <= today + timedelta(days=30):
#         return send_renewal_notice(instance)
#     return False

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from apps.core.models import Notification


def get_renewal_recipients(user=None):
    """Return staff members who should receive renewal notifications."""
    User = get_user_model()

    recipients = User.objects.filter(is_active=True).filter(
        is_staff=True
    )

    if user is not None and user.is_authenticated:
        recipients = recipients | User.objects.filter(pk=user.pk)

    return recipients.distinct()


def send_renewal_notice(instance, user=None):
    """
    Send a renewal email when needed, transition the lease to renewal,
    and notify the responsible staff members.
    """
    if instance.status != "active":
        return False

    tenant = instance.tenant
    email_sent = False

    # Send the email only if a notice has not already been recorded.
    if not instance.expiry_notice_sent and tenant.email:
        sent_count = send_mail(
            subject=f"Lease renewal notice: {instance.lease_number}",
            message=(
                f"Dear {tenant.full_name},\n\n"
                f"Your lease {instance.lease_number} for "
                f"{instance.unit.property.name}, "
                f"unit {instance.unit.unit_number}, expires on "
                f"{instance.end_date:%d %B %Y}.\n\n"
                "Please contact the Diocesan Estates Department "
                "to discuss renewal arrangements.\n\n"
                "Regards,\nDiocesan Estates Department"
            ),
            from_email=None,
            recipient_list=[tenant.email],
            fail_silently=False,
        )

        if sent_count == 1:
            instance.expiry_notice_sent = True
            email_sent = True

    # Transition the lease, even if the email was already sent previously.
    instance.status = "renewal"
    fields = ["status", "updated_at"]

    if instance.expiry_notice_sent:
        fields.append("expiry_notice_sent")

    instance.save(update_fields=fields)

    # Notify responsible staff. The command does not need a logged-in user.
    title = f"Lease renewal pending: {instance.lease_number}"

    if email_sent:
        email_message = f"A renewal email was sent to {tenant.email}."
    elif instance.expiry_notice_sent:
        email_message = (
            "The renewal notice was previously marked as sent. "
            "No duplicate email was sent."
        )
    elif not tenant.email:
        email_message = (
            "The tenant has no email address. "
            "Contact the tenant directly."
        )
    else:
        email_message = "The lease has entered renewal pending."

    message = (
        f"Lease {instance.lease_number} for "
        f"{instance.unit.property.name}, unit "
        f"{instance.unit.unit_number}, expires on "
        f"{instance.end_date:%d %B %Y}. "
        f"{email_message}"
    )

    for recipient in get_renewal_recipients(user):
        Notification.objects.get_or_create(
            user=recipient,
            title=title,
            message=message,
            defaults={"priority": "high"},
        )

    return True


def send_lease_expiry_reminder(instance, days_remaining, user=None):
    """Send the reminder for a lease at a configured expiry milestone.

    Expiry reminders are deliberately separate from ``send_renewal_notice``:
    sending a reminder must not move the lease into renewal status or consume
    the one-time ``expiry_notice_sent`` flag.  The management command runs on
    the milestone date, and the notification key makes a rerun idempotent.
    """
    if instance.status != "renewal":
        return False

    tenant = instance.tenant
    days_label = "day" if days_remaining == 1 else "days"
    title = f"Lease expires in {days_remaining} {days_label}: {instance.lease_number}"
    message = (
        f"Lease {instance.lease_number} for {instance.unit.property.name}, "
        f"unit {instance.unit.unit_number}, expires in {days_remaining} "
        f"{days_label} on {instance.end_date:%d %B %Y}."
    )

    if tenant.email:
        send_mail(
            subject=title,
            message=(
                f"Dear {tenant.full_name},\n\n{message}\n\n"
                "Please contact the Diocesan Estates Department to discuss "
                "renewal arrangements.\n\n"
                "Regards,\nDiocesan Estates Department"
            ),
            from_email=None,
            recipient_list=[tenant.email],
            fail_silently=False,
        )

    for recipient in get_renewal_recipients(user):
        Notification.objects.get_or_create(
            user=recipient,
            title=title,
            message=message,
            defaults={"priority": "high"},
        )

    return True


def process_renewal_window(instance, user=None, window_days=30):
    """Process active leases ending within the configured renewal window."""
    today = timezone.localdate()
    cutoff = today + timedelta(days=window_days)

    if (
        instance.status == "active"
        and today <= instance.end_date <= cutoff
    ):
        return send_renewal_notice(instance, user=user)

    return False
