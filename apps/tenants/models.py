from django.db import models
from apps.core.models import TimeStampedModel
from apps.properties.models import Unit

class Tenant(TimeStampedModel):
    STATUS=[("active","Active"),("inactive","Inactive"),("prospect","Prospect")]
    tenant_id=models.CharField(max_length=30,unique=True)
    full_name=models.CharField(max_length=180)
    phone=models.CharField(max_length=40)
    email=models.EmailField(blank=True)
    national_id=models.CharField(max_length=80,blank=True)
    address=models.TextField(blank=True)
    emergency_contact=models.CharField(max_length=180,blank=True)
    status=models.CharField(max_length=20,choices=STATUS,default="active")
    notes=models.TextField(blank=True)
    def __str__(self): return f"{self.tenant_id} — {self.full_name}"


class TenantUnit(TimeStampedModel):
    tenant=models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name="occupancies")
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE,related_name="occupancies")
    move_in=models.DateField(null=True,blank=True)
    move_out=models.DateField(null=True,blank=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=["-active","-move_in"]
