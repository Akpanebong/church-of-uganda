from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import Inspection, Asset, Contractor, Visitor, ComplianceItem, DevelopmentProject, LandDispute, RiskRegisterItem
from .models import UtilityMeter, MeterReading, ParkingSpace
from .forms import (InspectionForm, UtilityMeterForm, MeterReadingForm, AssetForm, ContractorForm, VisitorForm,
                    ParkingSpaceForm, ComplianceItemForm, DevelopmentProjectForm, LandDisputeForm, RiskRegisterItemForm)
from apps.core.crud import model_form_view, model_delete_view
from datetime import timedelta
from django.utils import timezone


@login_required
def operations(request):
    today = timezone.localdate()
    next_30_days = today + timedelta(days=30)

    # Inspections
    inspections = (
        Inspection.objects
        .select_related("property", "unit")
        .order_by("-inspection_date", "-created_at")[:8]
    )

    # Estate assets
    assets = (
        Asset.objects
        .select_related("property")
        .order_by("-created_at")[:8]
    )

    # Active contractors
    contractors = (
        Contractor.objects
        .filter(active=True)
        .order_by("name")[:8]
    )

    # Recent visitor activity
    visitors = (
        Visitor.objects
        .select_related("property")
        .order_by("-check_in")[:8]
    )

    # Expired, upcoming and undated compliance records
    compliance = (
        ComplianceItem.objects
        .select_related("property")
        .filter(
            Q(expiry_date__isnull=True)
            | Q(expiry_date__lte=next_30_days)
        )
        .order_by("expiry_date", "title")[:8]
    )

    # Projects requiring operational oversight
    projects = (
        DevelopmentProject.objects
        .select_related("property")
        .order_by("-created_at")[:6]
    )

    # Unresolved land disputes
    disputes = (
        LandDispute.objects
        .select_related("property")
        .exclude(status__in=["closed", "resolved"])
        .order_by("next_action_date", "-created_at")[:6]
    )

    # Risks requiring oversight
    risks = (
        RiskRegisterItem.objects
        .select_related("property")
        .exclude(status__iexact="closed")
        .order_by("review_date", "-created_at")[:6]
    )

    context = {
        # Shared date reference for template comparisons
        "today": today,
        "next_30_days": next_30_days,

        # Operational records
        "inspections": inspections,
        "assets": assets,
        "contractors": contractors,
        "visitors": visitors,
        "compliance": compliance,
        "projects": projects,
        "disputes": disputes,
        "risks": risks,

        # Dashboard KPI widgets
        "inspections_count": Inspection.objects.count(),
        "assets_count": Asset.objects.count(),
        "contractors_count": Contractor.objects.filter(active=True).count(),

        "expired_compliance_count": ComplianceItem.objects.filter(
            expiry_date__lt=today
        ).count(),

        "upcoming_compliance_count": ComplianceItem.objects.filter(
            expiry_date__gte=today,
            expiry_date__lte=next_30_days,
        ).count(),

        "active_projects_count": DevelopmentProject.objects.filter(
            status__in=["approved", "active"]
        ).count(),

        "open_disputes_count": LandDispute.objects.exclude(
            status__in=["closed", "resolved"]
        ).count(),

        "open_risks_count": RiskRegisterItem.objects.exclude(
            status__iexact="closed"
        ).count(),

        "active_visitors_count": Visitor.objects.filter(
            check_out__isnull=True
        ).count(),
    }

    return render(request, "operations/index.html", context)


@login_required
def inspection_register(request):
    return render(request, "operations/inspections.html", {"inspections": Inspection.objects.select_related("property", "unit").order_by("-inspection_date")})


@login_required
def project_register(request):
    return render(request, "operations/projects.html", {"projects": DevelopmentProject.objects.select_related("property").order_by("-created_at")})

@login_required
def dispute_register(request):
    return render(request, "operations/disputes.html", {"disputes": LandDispute.objects.select_related("property").order_by("-created_at")})

@login_required
def risk_register(request):
    return render(request, "operations/risks.html", {"risks": RiskRegisterItem.objects.select_related("property").order_by("-created_at")})

@login_required
def compliance_register(request):
    return render(request, "operations/compliance.html", {"compliance": ComplianceItem.objects.select_related("property").order_by("expiry_date")})

@login_required
def asset_register(request):
    return render(request, "operations/assets.html", {"assets": Asset.objects.select_related("property").order_by("-created_at")})
@login_required
def contractor_register(request):
    return render(request, "operations/contractors.html", {"contractors": Contractor.objects.order_by("name")})
@login_required
def visitor_register(request):
    return render(request, "operations/visitors.html", {"visitors": Visitor.objects.select_related("property").order_by("-check_in")})

@login_required
def asset_detail(request, pk):
    return render(request, "operations/asset_detail.html", {"asset": get_object_or_404(Asset.objects.select_related("property"), pk=pk)})
@login_required
def contractor_detail(request, pk):
    return render(request, "operations/contractor_detail.html", {"contractor": get_object_or_404(Contractor, pk=pk)})
@login_required
def visitor_detail(request, pk):
    return render(request, "operations/visitor_detail.html", {"visitor": get_object_or_404(Visitor.objects.select_related("property"), pk=pk)})

@login_required
def asset_trash(request, pk): return model_delete_view(request, Asset, "asset_register", pk, "Asset", "operations/asset_trash.html")
@login_required
def contractor_trash(request, pk): return model_delete_view(request, Contractor, "contractor_register", pk, "Contractor", "operations/contractor_trash.html")
@login_required
def visitor_trash(request, pk): return model_delete_view(request, Visitor, "visitor_register", pk, "Visitor", "operations/visitor_trash.html")
@login_required
def parking_register(request):
    return render(request, "operations/parking.html", {"spaces": ParkingSpace.objects.select_related("property").order_by("property__name", "space_number")})
@login_required
def meter_register(request):
    return render(request, "operations/meters.html", {"meters": UtilityMeter.objects.select_related("unit").order_by("meter_number")})
@login_required
def reading_register(request):
    return render(request, "operations/readings.html", {"readings": MeterReading.objects.select_related("meter", "meter__unit").order_by("-reading_date")})

def _crud(model, form, template, route, title, request, pk=None, delete=False):
    if delete: return model_delete_view(request, model, route, pk, title)
    return model_form_view(request, model, form, template, route, pk, title)

@login_required
def inspection_create(request): return _crud(Inspection, InspectionForm, "operations/inspection_form.html", "inspection_register", "Inspection", request)
@login_required
def inspection_update(request, pk): return _crud(Inspection, InspectionForm, "operations/inspection_form.html", "inspection_register", "Inspection", request, pk)
@login_required
def inspection_delete(request, pk): return _crud(Inspection, InspectionForm, "operations/inspection_form.html", "inspection_register", "Inspection", request, pk, True)
@login_required
def utility_meter_create(request): return _crud(UtilityMeter, UtilityMeterForm, "operations/utility_meter_form.html", "operations", "Utility meter", request)
@login_required
def utility_meter_update(request, pk): return _crud(UtilityMeter, UtilityMeterForm, "operations/utility_meter_form.html", "operations", "Utility meter", request, pk)
@login_required
def utility_meter_delete(request, pk): return _crud(UtilityMeter, UtilityMeterForm, "operations/utility_meter_form.html", "operations", "Utility meter", request, pk, True)
@login_required
def meter_reading_create(request): return _crud(MeterReading, MeterReadingForm, "operations/meter_reading_form.html", "operations", "Meter reading", request)
@login_required
def meter_reading_update(request, pk): return _crud(MeterReading, MeterReadingForm, "operations/meter_reading_form.html", "operations", "Meter reading", request, pk)
@login_required
def meter_reading_delete(request, pk): return _crud(MeterReading, MeterReadingForm, "operations/meter_reading_form.html", "operations", "Meter reading", request, pk, True)
@login_required
def asset_create(request): return _crud(Asset, AssetForm, "operations/asset_form.html", "operations", "Asset", request)
@login_required
def asset_update(request, pk): return _crud(Asset, AssetForm, "operations/asset_form.html", "operations", "Asset", request, pk)
@login_required
def asset_delete(request, pk): return asset_trash(request, pk)
@login_required
def contractor_create(request): return _crud(Contractor, ContractorForm, "operations/contractor_form.html", "operations", "Contractor", request)
@login_required
def contractor_update(request, pk): return _crud(Contractor, ContractorForm, "operations/contractor_form.html", "operations", "Contractor", request, pk)
@login_required
def contractor_delete(request, pk): return contractor_trash(request, pk)
@login_required
def visitor_create(request): return _crud(Visitor, VisitorForm, "operations/visitor_form.html", "operations", "Visitor", request)
@login_required
def visitor_update(request, pk): return _crud(Visitor, VisitorForm, "operations/visitor_form.html", "operations", "Visitor", request, pk)
@login_required
def visitor_delete(request, pk): return visitor_trash(request, pk)
@login_required
def parking_space_create(request): return _crud(ParkingSpace, ParkingSpaceForm, "operations/parking_space_form.html", "operations", "Parking space", request)
@login_required
def parking_space_update(request, pk): return _crud(ParkingSpace, ParkingSpaceForm, "operations/parking_space_form.html", "operations", "Parking space", request, pk)
@login_required
def parking_space_delete(request, pk): return _crud(ParkingSpace, ParkingSpaceForm, "operations/parking_space_form.html", "operations", "Parking space", request, pk, True)
@login_required
def compliance_create(request): return _crud(ComplianceItem, ComplianceItemForm, "operations/compliance_form.html", "compliance_register", "Compliance item", request)
@login_required
def compliance_update(request, pk): return _crud(ComplianceItem, ComplianceItemForm, "operations/compliance_form.html", "compliance_register", "Compliance item", request, pk)
@login_required
def compliance_delete(request, pk): return _crud(ComplianceItem, ComplianceItemForm, "operations/compliance_form.html", "compliance_register", "Compliance item", request, pk, True)
@login_required
def project_create(request): return _crud(DevelopmentProject, DevelopmentProjectForm, "operations/project_form.html", "project_register", "Development project", request)
@login_required
def project_update(request, pk): return _crud(DevelopmentProject, DevelopmentProjectForm, "operations/project_form.html", "project_register", "Development project", request, pk)
@login_required
def project_delete(request, pk): return _crud(DevelopmentProject, DevelopmentProjectForm, "operations/project_form.html", "project_register", "Development project", request, pk, True)
@login_required
def dispute_create(request): return _crud(LandDispute, LandDisputeForm, "operations/dispute_form.html", "dispute_register", "Land dispute", request)
@login_required
def dispute_update(request, pk): return _crud(LandDispute, LandDisputeForm, "operations/dispute_form.html", "dispute_register", "Land dispute", request, pk)
@login_required
def dispute_delete(request, pk): return _crud(LandDispute, LandDisputeForm, "operations/dispute_form.html", "dispute_register", "Land dispute", request, pk, True)
@login_required
def risk_create(request): return _crud(RiskRegisterItem, RiskRegisterItemForm, "operations/risk_form.html", "risk_register", "Risk item", request)
@login_required
def risk_update(request, pk): return _crud(RiskRegisterItem, RiskRegisterItemForm, "operations/risk_form.html", "risk_register", "Risk item", request, pk)
@login_required
def risk_delete(request, pk): return _crud(RiskRegisterItem, RiskRegisterItemForm, "operations/risk_form.html", "risk_register", "Risk item", request, pk, True)
