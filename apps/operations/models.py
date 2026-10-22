from django.db import models
from apps.core.models import TimeStampedModel
from apps.properties.models import Property, Unit

class Inspection(TimeStampedModel):
    TYPES=[("move_in","Move In"),("routine","Routine"),("move_out","Move Out"),("safety","Safety"),("maintenance","Maintenance")]
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="inspections")
    unit=models.ForeignKey(Unit,null=True,blank=True,on_delete=models.SET_NULL,related_name="inspections")
    inspection_type=models.CharField(max_length=30,choices=TYPES)
    inspection_date=models.DateField()
    inspector=models.CharField(max_length=180)
    condition=models.TextField()
    recommendations=models.TextField(blank=True)
    score=models.PositiveIntegerField(default=0)

class UtilityMeter(TimeStampedModel):
    TYPES=[("electricity","Electricity"),("water","Water"),("gas","Gas")]
    unit=models.ForeignKey(Unit,on_delete=models.CASCADE,related_name="meters")
    meter_number=models.CharField(max_length=80)
    utility_type=models.CharField(max_length=30,choices=TYPES)
    active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.meter_number} - {self.utility_type}"

class MeterReading(TimeStampedModel):
    meter=models.ForeignKey(UtilityMeter,on_delete=models.CASCADE,related_name="readings")
    reading_date=models.DateField()
    reading=models.DecimalField(max_digits=14,decimal_places=3)
    previous_reading=models.DecimalField(max_digits=14,decimal_places=3,default=0)
    notes=models.CharField(max_length=240,blank=True)

    def __str__(self):
        return f"{self.reading_date} - {self.reading}"

class Asset(TimeStampedModel):
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="assets")
    asset_code=models.CharField(max_length=40,unique=True)
    name=models.CharField(max_length=180)
    category=models.CharField(max_length=80)
    purchase_date=models.DateField(null=True,blank=True)
    purchase_cost=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    condition=models.CharField(max_length=50,default="Good")
    warranty_expiry=models.DateField(null=True,blank=True)
    notes=models.TextField(blank=True)

    def __str__(self):
        return f"{self.asset_code} - {self.name}"

class Contractor(TimeStampedModel):
    name=models.CharField(max_length=180)
    service=models.CharField(max_length=120)
    phone=models.CharField(max_length=50)
    email=models.EmailField(blank=True)
    address=models.TextField(blank=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.service}"

class Visitor(TimeStampedModel):
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="visitors")
    host_name=models.CharField(max_length=180)
    visitor_name=models.CharField(max_length=180)
    phone=models.CharField(max_length=50,blank=True)
    vehicle_registration=models.CharField(max_length=50,blank=True)
    purpose=models.CharField(max_length=240)
    check_in=models.DateTimeField()
    check_out=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.visitor_name} - {self.host_name}"

class ParkingSpace(TimeStampedModel):
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="parking_spaces")
    space_number=models.CharField(max_length=50)
    assigned_to=models.CharField(max_length=180,blank=True)
    vehicle_registration=models.CharField(max_length=50,blank=True)
    monthly_fee=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.space_number} - {self.assigned_to}"

class ComplianceItem(TimeStampedModel):
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name="compliance_items")
    title=models.CharField(max_length=180)
    reference=models.CharField(max_length=100,blank=True)
    expiry_date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=40,default="Valid")
    notes=models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.reference}"

class DevelopmentProject(TimeStampedModel):
    STATUS=[("proposed","Proposed"),("approved","Approved"),("active","Active"),
            ("on_hold","On hold"),("completed","Completed"),("cancelled","Cancelled")]
    project_code=models.CharField(max_length=40,unique=True)
    property=models.ForeignKey(Property,on_delete=models.PROTECT,related_name="development_projects")
    name=models.CharField(max_length=180)
    sponsor=models.CharField(max_length=180,blank=True)
    description=models.TextField(blank=True)
    status=models.CharField(max_length=20,choices=STATUS,default="proposed")
    start_date=models.DateField(null=True,blank=True)
    target_date=models.DateField(null=True,blank=True)
    approved_budget=models.DecimalField(max_digits=15,decimal_places=2,default=0)
    spent_amount=models.DecimalField(max_digits=15,decimal_places=2,default=0)
    approval_reference=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.project_code} - {self.name}"

class LandDispute(TimeStampedModel):
    STATUS=[("open","Open"),("mediation","In mediation"),("court","In court"),
            ("resolved","Resolved"),("closed","Closed")]
    reference=models.CharField(max_length=40,unique=True)
    property=models.ForeignKey(Property,on_delete=models.PROTECT,related_name="disputes")
    claimant=models.CharField(max_length=180)
    summary=models.TextField()
    status=models.CharField(max_length=20,choices=STATUS,default="open")
    assigned_officer=models.CharField(max_length=180,blank=True)
    next_action_date=models.DateField(null=True,blank=True)
    resolution=models.TextField(blank=True)

    def __str__(self):
        return f"{self.reference} - {self.claimant}"

class RiskRegisterItem(TimeStampedModel):
    LEVELS=[("low","Low"),("medium","Medium"),("high","High"),("critical","Critical")]
    reference=models.CharField(max_length=40,unique=True)
    property=models.ForeignKey(Property,null=True,blank=True,on_delete=models.SET_NULL,related_name="risks")
    risk_title=models.CharField(max_length=180)
    description=models.TextField()
    likelihood=models.CharField(max_length=20,choices=LEVELS,default="medium")
    impact=models.CharField(max_length=20,choices=LEVELS,default="medium")
    mitigation=models.TextField(blank=True)
    owner=models.CharField(max_length=180,blank=True)
    review_date=models.DateField(null=True,blank=True)
    status=models.CharField(max_length=30,default="Open")

    def __str__(self):
        return f"{self.reference} - {self.risk_title}"

