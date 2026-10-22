from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse
from apps.properties.models import Property, Unit
from apps.tenants.models import Tenant
from apps.leases.models import Lease
from apps.finance.models import Invoice, Payment, Expense
from apps.maintenance.models import MaintenanceRequest
from apps.operations.models import (
    DevelopmentProject,
    LandDispute,
    RiskRegisterItem,
    Inspection,
    Asset,
    Contractor,
    Visitor,
    ComplianceItem,
)
from .models import DioceseProfile, EstateDocument, Notification, AuditLog
from .forms import DioceseProfileForm, EstateDocumentForm
from .crud import model_form_view, model_delete_view
from django.shortcuts import redirect
from datetime import timedelta
from decimal import Decimal
from django.db.models import (Case, Count, DecimalField, ExpressionWrapper, F, Q, Sum, Value, When,)
from django.db.models.functions import Coalesce
from django.utils import timezone


@login_required
def dashboard(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    next_30_days = today + timedelta(days=30)
    next_7_days = today + timedelta(days=7)

    money_field = DecimalField(max_digits=16, decimal_places=2)
    zero_money = Value(Decimal("0.00"), output_field=money_field)

    # ---------------------------------------------------------
    # Portfolio
    # ---------------------------------------------------------
    properties = Property.objects.all()
    units = Unit.objects.all()

    properties_count = properties.count()
    active_properties = properties.filter(status="active").count()
    units_count = units.count()

    occupied_units = units.filter(status="occupied").count()
    vacant_units = units.filter(status="available").count()
    reserved_units = units.filter(status="reserved").count()
    maintenance_units = units.filter(status="maintenance").count()

    occupancy_rate = round(
        occupied_units / units_count * 100, 1
    ) if units_count else 0

    # ---------------------------------------------------------
    # Finance: invoices, receipts and expenditure
    # ---------------------------------------------------------
    invoices = Invoice.objects.exclude(status="cancelled")

    # Clamp each invoice's outstanding balance to zero.
    invoice_balance = Case(
        When(
            paid_amount__lt=F("amount"),
            then=ExpressionWrapper(
                F("amount") - F("paid_amount"),
                output_field=money_field,
            ),
        ),
        default=zero_money,
        output_field=money_field,
    )

    receivables = invoices.aggregate(
        total=Coalesce(Sum(invoice_balance), zero_money),
    )["total"]

    overdue_invoices = invoices.filter(
        due_date__lt=today,
        paid_amount__lt=F("amount"),
    )

    overdue_balance = overdue_invoices.aggregate(
        total=Coalesce(Sum(invoice_balance), zero_money),
    )["total"]

    outstanding_invoices = invoices.filter(
        paid_amount__lt=F("amount"),
    )

    payments = Payment.objects.all()
    monthly_payments = payments.filter(
        payment_date__gte=month_start,
        payment_date__lte=today,
    )
    monthly_collections = monthly_payments.aggregate(
        total=Coalesce(Sum("amount"), zero_money),
    )["total"]

    previous_month_start = (
        (month_start - timedelta(days=1)).replace(day=1)
    )
    previous_month_end = month_start - timedelta(days=1)

    previous_month_collections = payments.filter(
        payment_date__gte=previous_month_start,
        payment_date__lte=previous_month_end,
    ).aggregate(
        total=Coalesce(Sum("amount"), zero_money),
    )["total"]

    monthly_expenses = Expense.objects.filter(
        expense_date__gte=month_start,
        expense_date__lte=today,
    ).aggregate(
        total=Coalesce(Sum("amount"), zero_money),
    )["total"]

    monthly_net_cashflow = monthly_collections - monthly_expenses

    # ---------------------------------------------------------
    # Tenants and leases
    # ---------------------------------------------------------
    tenants_count = Tenant.objects.filter(status="active").count()

    active_leases = Lease.objects.filter(status="active")
    expiring_leases = active_leases.filter(
        end_date__gte=today,
        end_date__lte=next_30_days,
    )

    expired_unresolved_leases = Lease.objects.filter(
        end_date__lt=today,
        status="active",
    )

    # ---------------------------------------------------------
    # Maintenance and inspections
    # ---------------------------------------------------------
    maintenance = MaintenanceRequest.objects.exclude(
        status__in=["completed", "closed"],
    )

    urgent_maintenance = maintenance.filter(
        priority__in=["high", "urgent"],
    )

    maintenance_costs = maintenance.aggregate(
        estimated=Coalesce(Sum("estimated_cost"), zero_money),
        actual=Coalesce(Sum("actual_cost"), zero_money),
    )

    inspections_due = Inspection.objects.filter(
        inspection_date__gte=today,
        inspection_date__lte=next_30_days,
    )

    # ---------------------------------------------------------
    # Development projects and property assets
    # ---------------------------------------------------------
    projects = DevelopmentProject.objects.all()
    active_projects = projects.filter(
        status__in=["approved", "active"],
    )

    over_budget_projects = active_projects.filter(
        approved_budget__gt=0,
        spent_amount__gt=F("approved_budget"),
    )

    total_project_budget = active_projects.aggregate(
        total=Coalesce(Sum("approved_budget"), zero_money),
    )["total"]

    total_project_spend = active_projects.aggregate(
        total=Coalesce(Sum("spent_amount"), zero_money),
    )["total"]

    assets_count = Asset.objects.count()
    assets_needing_attention = Asset.objects.filter(
        Q(warranty_expiry__lt=today)
        | Q(condition__icontains="poor")
        | Q(condition__icontains="damaged")
        | Q(condition__icontains="repair")
    )

    # ---------------------------------------------------------
    # Governance, compliance and risk
    # ---------------------------------------------------------
    open_disputes = LandDispute.objects.exclude(
        status__in=["resolved", "closed"],
    )

    critical_risks = RiskRegisterItem.objects.filter(
        likelihood__in=["high", "critical"],
        impact__in=["high", "critical"],
    ).exclude(status__iexact="closed")

    risks_due = RiskRegisterItem.objects.filter(
        review_date__lte=next_30_days,
    ).exclude(status__iexact="closed")

    compliance_items = ComplianceItem.objects.all()
    expired_compliance = compliance_items.filter(
        expiry_date__lt=today,
    ).exclude(status__iexact="expired")

    expiring_compliance = compliance_items.filter(
        expiry_date__gte=today,
        expiry_date__lte=next_30_days,
    ).exclude(status__iexact="expired")

    missing_title_references = properties.filter(
        title_reference="",
    ).count()

    documents_count = EstateDocument.objects.count()
    confidential_documents = EstateDocument.objects.filter(
        is_confidential=True,
    ).count()

    # ---------------------------------------------------------
    # Security, audit and notifications
    # ---------------------------------------------------------
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False,
    )

    recent_audit_logs = AuditLog.objects.select_related(
        "user",
    ).order_by("-created_at")[:8]

    recent_payments = payments.select_related(
        "tenant",
        "invoice",
    ).order_by("-payment_date", "-created_at")[:7]

    recent_maintenance = MaintenanceRequest.objects.select_related(
        "unit",
        "unit__property",
        "reported_by",
    ).exclude(
        status__in=["completed", "closed"],
    ).order_by(
        "-created_at",
    )[:6]

    recent_projects = active_projects.select_related(
        "property",
    ).order_by(
        "target_date",
        "-created_at",
    )[:5]

    recent_disputes = open_disputes.select_related(
        "property",
    ).order_by(
        "next_action_date",
        "-created_at",
    )[:5]

    recent_overdue_invoices = overdue_invoices.select_related(
        "tenant",
        "unit",
    ).order_by(
        "due_date",
    )[:5]

    recent_compliance = compliance_items.filter(
        Q(expiry_date__lt=today)
        | Q(expiry_date__lte=next_30_days)
    ).order_by(
        "expiry_date",
    )[:5]

    recent_notifications = unread_notifications.order_by(
        "-created_at",
    )[:5]

    # ---------------------------------------------------------
    # Executive dashboard context
    # ---------------------------------------------------------
    context = {
        "today": today,

        # Portfolio
        "properties_count": properties_count,
        "active_properties": active_properties,
        "units_count": units_count,
        "occupied_units": occupied_units,
        "vacant_units": vacant_units,
        "reserved_units": reserved_units,
        "maintenance_units": maintenance_units,
        "occupancy_rate": occupancy_rate,
        "tenants_count": tenants_count,

        # Finance
        "outstanding": receivables,
        "overdue_balance": overdue_balance,
        "outstanding_invoices_count": outstanding_invoices.count(),
        "overdue_invoices_count": overdue_invoices.count(),
        "monthly_collections": monthly_collections,
        "previous_month_collections": previous_month_collections,
        "monthly_expenses": monthly_expenses,
        "monthly_net_cashflow": monthly_net_cashflow,

        # Leasing
        "active_leases": active_leases.count(),
        "leases_expiring": expiring_leases.count(),
        "expired_unresolved_leases": expired_unresolved_leases.count(),

        # Operations
        "open_maintenance": maintenance.count(),
        "urgent_maintenance": urgent_maintenance.count(),
        "maintenance_estimated_cost": maintenance_costs["estimated"],
        "maintenance_actual_cost": maintenance_costs["actual"],
        "inspections_due": inspections_due.count(),

        # Projects and assets
        "active_projects": active_projects.count(),
        "over_budget_projects": over_budget_projects.count(),
        "total_project_budget": total_project_budget,
        "total_project_spend": total_project_spend,
        "assets_count": assets_count,
        "assets_needing_attention": assets_needing_attention.count(),

        # Governance
        "open_disputes": open_disputes.count(),
        "critical_risks": critical_risks.count(),
        "risks_due": risks_due.count(),
        "expired_compliance": expired_compliance.count(),
        "expiring_compliance": expiring_compliance.count(),
        "missing_title_references": missing_title_references,
        "documents_count": documents_count,
        "confidential_documents": confidential_documents,

        # Recent records
        "recent_payments": recent_payments,
        "recent_maintenance": recent_maintenance,
        "recent_projects": recent_projects,
        "recent_disputes": recent_disputes,
        "recent_overdue_invoices": recent_overdue_invoices,
        "recent_compliance": recent_compliance,
        "recent_audit_logs": recent_audit_logs,
        "unread_notifications_count": unread_notifications.count(),
        "recent_notifications": recent_notifications,
    }

    return render(request, "dashboard.html", context)

# @login_required
# def dashboard(request):
#     context = {
#         "properties_count": Property.objects.count(),
#         "units_count": Unit.objects.count(),
#         "occupied_units": Unit.objects.filter(status="occupied").count(),
#         "vacant_units": Unit.objects.filter(status="available").count(),
#         "tenants_count": Tenant.objects.filter(status="active").count(),
#         "leases_expiring": Lease.objects.filter(status="active").count(),
#         "open_maintenance": MaintenanceRequest.objects.exclude(status="closed").count(),
#         "outstanding": Invoice.objects.filter(status__in=["unpaid", "partial"]).aggregate(
#             v=Sum(
#                 ExpressionWrapper(
#                     F("amount") - F("paid_amount"),
#                     output_field=DecimalField(max_digits=14, decimal_places=2),
#                 )
#             )
#         )["v"] or 0,
#         "recent_payments": Payment.objects.select_related("tenant").order_by("-payment_date")[:7],
#         "recent_maintenance": MaintenanceRequest.objects.select_related("unit","reported_by").order_by("-created_at")[:6],
#         "active_projects": DevelopmentProject.objects.filter(status__in=["approved", "active"]).count(),
#         "open_disputes": LandDispute.objects.exclude(status__in=["resolved", "closed"]).count(),
#         "critical_risks": RiskRegisterItem.objects.filter(likelihood__in=["high", "critical"], impact__in=["high", "critical"]).exclude(status="Closed").count(),
#     }
#     return render(request, "dashboard.html", context)

@login_required
def notifications(request):
    items = request.user.notifications.all()[:50]
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return render(request, "core/notifications.html", {"items": items})

@login_required
def global_search(request):
    query = (request.GET.get("q") or "").strip()
    results = []
    if query:
        term = Q(name__icontains=query) | Q(code__icontains=query)
        results += [{"type": "Property", "title": p.name, "meta": p.code, "url": "property_detail", "pk": p.pk} for p in Property.objects.filter(term)[:10]]
        tenant_term = Q(full_name__icontains=query) | Q(tenant_id__icontains=query) | Q(phone__icontains=query)
        results += [{"type": "Tenant", "title": t.full_name, "meta": t.tenant_id, "url": "tenant_update", "pk": t.pk} for t in Tenant.objects.filter(tenant_term)[:10]]
        lease_term = Q(lease_number__icontains=query) | Q(tenant__full_name__icontains=query) | Q(unit__unit_number__icontains=query)
        results += [{"type": "Lease", "title": l.lease_number, "meta": l.tenant.full_name, "url": "lease_update", "pk": l.pk} for l in Lease.objects.select_related("tenant").filter(lease_term)[:10]]
        invoice_term = Q(invoice_number__icontains=query) | Q(description__icontains=query) | Q(tenant__full_name__icontains=query)
        results += [{"type": "Invoice", "title": i.invoice_number, "meta": i.tenant.full_name, "url": "invoice_update", "pk": i.pk} for i in Invoice.objects.select_related("tenant").filter(invoice_term)[:10]]
        payment_term = Q(receipt_number__icontains=query) | Q(reference__icontains=query) | Q(tenant__full_name__icontains=query)
        results += [{"type": "Payment", "title": p.receipt_number, "meta": p.tenant.full_name, "url": "payment_update", "pk": p.pk} for p in Payment.objects.select_related("tenant").filter(payment_term)[:10]]
        expense_term = Q(description__icontains=query) | Q(category__icontains=query) | Q(vendor__icontains=query) | Q(reference__icontains=query)
        results += [{"type": "Expense", "title": e.description, "meta": e.category, "url": "expense_update", "pk": e.pk} for e in Expense.objects.filter(expense_term)[:10]]
        asset_term = Q(name__icontains=query) | Q(asset_code__icontains=query) | Q(category__icontains=query)
        results += [{"type": "Asset", "title": a.name, "meta": a.asset_code, "url": "asset_detail", "pk": a.pk} for a in Asset.objects.filter(asset_term)[:10]]
        contractor_term = Q(name__icontains=query) | Q(service__icontains=query) | Q(phone__icontains=query)
        results += [{"type": "Contractor", "title": c.name, "meta": c.service, "url": "contractor_detail", "pk": c.pk} for c in Contractor.objects.filter(contractor_term)[:10]]
        visitor_term = Q(visitor_name__icontains=query) | Q(host_name__icontains=query) | Q(phone__icontains=query) | Q(vehicle_registration__icontains=query)
        results += [{"type": "Visitor", "title": v.visitor_name, "meta": v.property.name, "url": "visitor_detail", "pk": v.pk} for v in Visitor.objects.select_related("property").filter(visitor_term)[:10]]
    if request.GET.get("format") == "json" or request.headers.get("x-requested-with") == "XMLHttpRequest":
        for result in results:
            result["href"] = reverse(result["url"], args=[result["pk"]])
        return JsonResponse({"results": results[:15]})
    return render(request, "core/search_results.html", {"query": query, "results": results})

@login_required
def diocese_profile(request):
    return redirect("diocese_profile_list")

@login_required
def diocese_profile_list(request):
    return render(request, "core/diocese_profiles.html", {"profiles": DioceseProfile.objects.order_by("-is_active", "-created_at")})

@login_required
def diocese_profile_detail(request, pk):
    return render(request, "core/diocese_profile_detail.html", {"profile": get_object_or_404(DioceseProfile, pk=pk)})

@login_required
def diocese_profile_create(request):
    return model_form_view(request, DioceseProfile, DioceseProfileForm, "core/diocese_profile_form.html", "diocese_profile_list", title="Diocese profile")

@login_required
def diocese_profile_update(request, pk):
    return model_form_view(request, DioceseProfile, DioceseProfileForm, "core/diocese_profile_form.html", "diocese_profile_list", pk, "Diocese profile")

@login_required
def diocese_profile_trash(request, pk):
    return model_delete_view(request, DioceseProfile, "diocese_profile_list", pk, "Diocese profile", "core/diocese_profile_trash.html")

@login_required
def diocese_profile_delete(request, pk):
    return diocese_profile_trash(request, pk)

@login_required
def estate_document_list(request):
    return render(request, "core/estate_documents.html", {"documents": EstateDocument.objects.select_related("property").order_by("-created_at")})
@login_required
def estate_document_create(request): return model_form_view(request, EstateDocument, EstateDocumentForm, "core/estate_document_form.html", "estate_document_list", title="Estate document")
@login_required
def estate_document_update(request, pk): return model_form_view(request, EstateDocument, EstateDocumentForm, "core/estate_document_form.html", "estate_document_list", pk, "Estate document")
@login_required
def estate_document_delete(request, pk): return model_delete_view(request, EstateDocument, "estate_document_list", pk, "Estate document")
