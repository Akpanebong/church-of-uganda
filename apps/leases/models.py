from django.db import models
from apps.core.models import TimeStampedModel
from apps.tenants.models import Tenant
from apps.properties.models import Unit

class Lease(TimeStampedModel):
    STATUS=[("draft","Draft"),("active","Active"),("expired","Expired"),("terminated","Terminated"),("renewal","Renewal Pending")]
    lease_number=models.CharField(max_length=40,unique=True)
    tenant=models.ForeignKey(Tenant,on_delete=models.PROTECT,related_name="leases")
    unit=models.ForeignKey(Unit,on_delete=models.PROTECT,related_name="leases")
    start_date=models.DateField()
    end_date=models.DateField()
    rent=models.DecimalField(max_digits=14,decimal_places=2)
    deposit=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    service_charge=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    payment_frequency=models.CharField(max_length=30,default="Monthly")
    notice_period_days=models.PositiveIntegerField(default=30)
    status=models.CharField(max_length=30,choices=STATUS,default="draft")
    terms=models.TextField(blank=True)
    expiry_notice_sent=models.BooleanField(default=False)

    def __str__(self):
        return self.lease_number
