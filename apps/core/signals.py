from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import Notification
from apps.leases.models import Lease
from apps.maintenance.models import MaintenanceRequest

def _notify_staff(title, message, url):
    User = get_user_model()
    recipients = User.objects.filter(is_staff=True, is_active=True)
    Notification.objects.bulk_create([
        Notification(user=user, title=title, message=message, url=url, priority="high")
        for user in recipients
    ])

@receiver(post_save, sender=MaintenanceRequest)
def maintenance_request_created(sender, instance, created, **kwargs):
    if created:
        _notify_staff("New maintenance request", f"{instance.request_number} requires review.", "/maintenance/")

@receiver(post_save, sender=Lease)
def lease_created(sender, instance, created, **kwargs):
    if created:
        _notify_staff("Lease record created", f"Lease {instance.lease_number} was added to the register.", "/leases/")
