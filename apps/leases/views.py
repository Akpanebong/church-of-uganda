from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from apps.properties.models import Unit
from .models import Lease
from .forms import LeaseForm
from apps.core.crud import model_form_view, model_delete_view
from datetime import timedelta
from django.utils import timezone


@login_required
def lease_list(request):
    today = timezone.localdate()
    expiry_cutoff = today + timedelta(days=40)

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
            status="active",
            end_date__gte=today,
            end_date__lte=expiry_cutoff,
        ).count(),
        "past_end_date": Lease.objects.filter(
            status="active",
            end_date__lt=today,
        ).count(),
    }

    return render(request, "leases/list.html", context)


@login_required
def lease_create(request):
    return model_form_view(request, Lease, LeaseForm, "leases/lease_form.html",
                           "lease_list", title="Lease")


@login_required
def lease_update(request, pk):
    return model_form_view(request, Lease, LeaseForm, "leases/lease_form.html",
                           "lease_list", pk, "Lease")


@login_required
def lease_delete(request, pk):
    return model_delete_view(request, Lease, "lease_list", pk, "Lease")


@login_required
def unit_details(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    return JsonResponse({"unit_number": unit.unit_number, "monthly_rent": str(unit.monthly_rent),
                         "service_charge": str(unit.service_charge), "property": unit.property.name})
