from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from apps.properties.models import Unit
from .models import Lease
from .services import sync_lease


@receiver(post_save, sender=Lease)
def lease_saved(sender, instance, **kwargs):
    sync_lease(instance)


@receiver(post_delete, sender=Lease)
def lease_deleted(sender, instance, **kwargs):
    """Release the unit when its last active/renewal lease is deleted."""
    if not instance.unit_id:
        return

    has_current_lease = Lease.objects.filter(
        unit_id=instance.unit_id,
        status__in=["active", "renewal"],
    ).exists()
    if not has_current_lease:
        Unit.objects.filter(pk=instance.unit_id).update(status="available")
