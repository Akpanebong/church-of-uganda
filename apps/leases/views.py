from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from apps.properties.models import Unit
from .models import Lease
from .forms import LeaseForm
from apps.core.crud import model_form_view, model_delete_view
from apps.core.utils import audit
from apps.finance.models import Payment
from datetime import timedelta
from django.utils import timezone


@login_required
def lease_list(request):
    today = timezone.localdate()
    expiry_cutoff = today + timedelta(days=30)
    expiring_statuses = ["active", "renewal"]

    leases = (
        Lease.objects
        .select_related("tenant", "unit", "unit__property")
        .order_by("end_date", "-start_date")
    )

    context = {
        "leases": leases,
        "today": today,
        "expiry_cutoff": expiry_cutoff,

        # Summary metrics
        "total_leases": Lease.objects.count(),
        "active_leases": Lease.objects.filter(status="active").count(),
        "expiring_soon": Lease.objects.filter(
            status__in=expiring_statuses,
            end_date__gte=today,
            end_date__lte=expiry_cutoff,
        ).count(),
        "past_end_date": Lease.objects.filter(
            status__in=expiring_statuses,
            end_date__lt=today,
        ).count(),
    }

    return render(request, "leases/list.html", context)


@login_required
def lease_create(request):
    form = LeaseForm(
        data=request.POST if request.method == "POST" else None,
        files=request.FILES if request.method == "POST" else None,
        include_initial_payment=True,
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            lease = form.save()
            payment_amount = lease.deposit
            if payment_amount:
                Payment.objects.create(
                    tenant=lease.tenant,
                    invoice=lease.invoice,
                    payment_date=form.cleaned_data["initial_payment_date"],
                    amount=payment_amount,
                    method=form.cleaned_data["initial_payment_method"],
                    notes=f"Initial payment for lease {lease.lease_number}",
                )
            audit(request.user, "created", lease, "Lease created successfully.", request)
        message = "Lease created successfully."
        if payment_amount:
            message = "Lease created and initial payment recorded successfully."
        messages.success(request, message)
        return redirect("lease_list")

    return render(request, "leases/lease_form.html", {
        "form": form,
        "object": None,
        "page_title": "Create Lease",
        "is_update": False,
    })


@login_required
def lease_update(request, pk):
    return model_form_view(request, Lease, LeaseForm, "leases/lease_form.html",
                           "lease_list", pk, "Lease",
                           form_kwargs={"include_initial_payment": False})


@login_required
def lease_delete(request, pk):
    return model_delete_view(request, Lease, "lease_list", pk, "Lease")


@login_required
def unit_details(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    return JsonResponse({"unit_number": unit.unit_number, "monthly_rent": str(unit.monthly_rent),
                         "service_charge": str(unit.service_charge), "property": unit.property.name})
