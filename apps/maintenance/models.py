from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedModel
from apps.properties.models import Unit

class MaintenanceRequest(TimeStampedModel):
    PRIORITY=[("low","Low"),("normal","Normal"),("high","High"),("urgent","Urgent")]
    STATUS=[("reported","Reported"),("assigned","Assigned"),("progress","In Progress"),("parts","Awaiting Parts"),("completed","Completed"),("closed","Closed")]
    request_number=models.CharField(max_length=40,unique=True)
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE,related_name="maintenance_requests")
    reported_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    category=models.CharField(max_length=80)
    description=models.TextField()
    priority=models.CharField(max_length=20,choices=PRIORITY,default="normal")
    status=models.CharField(max_length=20,choices=STATUS,default="reported")
    estimated_cost=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    actual_cost=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    scheduled_date=models.DateField(null=True,blank=True)
    completed_date=models.DateField(null=True,blank=True)
    assigned_to=models.CharField(max_length=180,blank=True)
    def __str__(self): return self.request_number
