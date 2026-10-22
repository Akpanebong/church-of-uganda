from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Tenant, TenantUnit
from .forms import TenantForm, TenantUnitForm
from apps.core.crud import model_form_view, model_delete_view
@login_required
def tenant_list(request):
    qs=Tenant.objects.all().order_by("full_name")
    q=request.GET.get("q","")
    if q: qs=qs.filter(full_name__icontains=q) | qs.filter(tenant_id__icontains=q) | qs.filter(phone__icontains=q)
    return render(request,"tenants/list.html",{"tenants":qs})

@login_required
def tenant_create(request): return model_form_view(request, Tenant, TenantForm, "tenants/tenant_form.html", "tenant_list", title="Tenant")
@login_required
def tenant_update(request, pk): return model_form_view(request, Tenant, TenantForm, "tenants/tenant_form.html", "tenant_list", pk, "Tenant")
@login_required
def tenant_delete(request, pk): return model_delete_view(request, Tenant, "tenant_list", pk, "Tenant")
@login_required
def tenant_unit_create(request): return model_form_view(request, TenantUnit, TenantUnitForm, "tenants/tenant_unit_form.html", "tenant_list", title="Tenant occupancy")
@login_required
def tenant_unit_update(request, pk): return model_form_view(request, TenantUnit, TenantUnitForm, "tenants/tenant_unit_form.html", "tenant_list", pk, "Tenant occupancy")
@login_required
def tenant_unit_delete(request, pk): return model_delete_view(request, TenantUnit, "tenant_list", pk, "Tenant occupancy")

@login_required
def occupancy_list(request):
    qs = TenantUnit.objects.select_related("tenant", "unit", "unit__property").order_by("-active", "-move_in")
    return render(request, "tenants/occupancies.html", {"occupancies": qs})
