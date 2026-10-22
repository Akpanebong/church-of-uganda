from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import MaintenanceRequest
from .forms import MaintenanceRequestForm
from apps.core.crud import model_form_view, model_delete_view
@login_required
def maintenance_list(request):
    qs=MaintenanceRequest.objects.select_related("unit").order_by("-created_at")
    return render(request,"maintenance/list.html",{"requests":qs})

@login_required
def maintenance_create(request): return model_form_view(request, MaintenanceRequest, MaintenanceRequestForm, "maintenance/maintenance_form.html", "maintenance_list", title="Maintenance request")
@login_required
def maintenance_update(request, pk): return model_form_view(request, MaintenanceRequest, MaintenanceRequestForm, "maintenance/maintenance_form.html", "maintenance_list", pk, "Maintenance request")
@login_required
def maintenance_delete(request, pk): return model_delete_view(request, MaintenanceRequest, "maintenance_list", pk, "Maintenance request")
