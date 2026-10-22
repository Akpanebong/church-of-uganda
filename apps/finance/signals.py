from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Payment

def sync_invoice(invoice):
    if not invoice:
        return
    paid = invoice.payments.aggregate(total=Sum("amount"))["total"] or 0
    invoice.paid_amount = paid
    if invoice.status != "cancelled":
        if paid >= invoice.amount:
            invoice.status = "paid"
        elif paid > 0:
            invoice.status = "partial"
        elif invoice.due_date < timezone.localdate():
            invoice.status = "overdue"
        else:
            invoice.status = "unpaid"
    invoice.save(update_fields=["paid_amount", "status", "updated_at"])

@receiver([post_save, post_delete], sender=Payment)
def payment_saved(sender, instance, **kwargs):
    sync_invoice(instance.invoice)
