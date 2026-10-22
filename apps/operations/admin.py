from django.contrib import admin
from .models import Inspection, UtilityMeter, MeterReading, Asset, Contractor, Visitor, ParkingSpace, ComplianceItem, DevelopmentProject, LandDispute, RiskRegisterItem
admin.site.register([Inspection, UtilityMeter, MeterReading, Asset, Contractor, Visitor, ParkingSpace, ComplianceItem, DevelopmentProject, LandDispute, RiskRegisterItem])
