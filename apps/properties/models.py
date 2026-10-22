from django.db import models
from apps.core.models import TimeStampedModel

class Property(TimeStampedModel):
    TYPES = [("residential","Residential"),("commercial","Commercial"),("office","Office"),("retail","Retail"),("industrial","Industrial"),("mixed","Mixed Use"),("land","Land")]
    STATUS = [("active","Active"),("inactive","Inactive"),("development","Under Development")]
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=180)
    property_type = models.CharField(max_length=30, choices=TYPES)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default="Uganda")
    owner_name = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="active")
    purchase_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tenure_type = models.CharField(max_length=40, default="Church owned")
    title_reference = models.CharField(max_length=100, blank=True)
    parish = models.CharField(max_length=120, blank=True)
    archdeaconry = models.CharField(max_length=120, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    acquisition_date = models.DateField(null=True, blank=True)
    protected = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} — {self.name}"


class Building(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="buildings")
    name = models.CharField(max_length=120)
    floors = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.property.code} / {self.name}"


class Unit(TimeStampedModel):
    STATUS = [("available","Available"),("occupied","Occupied"),("reserved","Reserved"),("maintenance","Maintenance"),("unavailable","Unavailable")]
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="units")
    building = models.ForeignKey(Building, null=True, blank=True, on_delete=models.SET_NULL, related_name="units")
    unit_number = models.CharField(max_length=50)
    floor = models.CharField(max_length=30, blank=True)
    unit_type = models.CharField(max_length=80, default="Apartment")
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqm = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_rent = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default="available")

    def __str__(self):
        return f"{self.property.code} — {self.unit_number}"

    class Meta:
        unique_together = ("property","unit_number")
