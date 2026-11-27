from django.db import migrations


def align_due_dates(apps, schema_editor):
    Invoice = apps.get_model("finance", "Invoice")
    for invoice in Invoice.objects.select_related("lease").filter(lease__isnull=False):
        if invoice.due_date != invoice.lease.end_date:
            invoice.due_date = invoice.lease.end_date
            invoice.save(update_fields=["due_date", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0002_invoice_lease"),
    ]

    operations = [
        migrations.RunPython(align_due_dates, migrations.RunPython.noop),
    ]
