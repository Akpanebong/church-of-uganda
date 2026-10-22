from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lease
from .services import sync_lease


@receiver(post_save, sender=Lease)
def lease_saved(sender, instance, **kwargs):
    sync_lease(instance)
