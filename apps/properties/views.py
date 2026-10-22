from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from .models import Property, Unit
from .models import Building
from .forms import PropertyForm, BuildingForm, UnitForm
from apps.core.crud import model_form_view, model_delete_view

@login_required
def property_list(request):
    qs = Property.objects.annotate(unit_count=Count("units")).order_by("name")
    q = request.GET.get("q","")
    if q: qs = qs.filter(name__icontains=q) | qs.filter(code__icontains=q)
    return render(request, "properties/list.html", {"properties": qs})

@login_required
def property_detail(request, pk):
    obj = get_object_or_404(Property, pk=pk)
    return render(request, "properties/detail.html", {"property": obj})

@login_required
def property_create(request): return model_form_view(request, Property, PropertyForm, "properties/property_form.html", "property_list", title="Property")
@login_required
def property_update(request, pk): return model_form_view(request, Property, PropertyForm, "properties/property_form.html", "property_list", pk, "Property")
@login_required
def property_delete(request, pk): return model_delete_view(request, Property, "property_list", pk, "Property")
@login_required
def building_create(request): return model_form_view(request, Building, BuildingForm, "properties/building_form.html", "property_list", title="Building")
@login_required
def building_update(request, pk): return model_form_view(request, Building, BuildingForm, "properties/building_form.html", "property_list", pk, "Building")
@login_required
def building_delete(request, pk): return model_delete_view(request, Building, "property_list", pk, "Building")
@login_required
def unit_create(request): return model_form_view(request, Unit, UnitForm, "properties/unit_form.html", "property_list", title="Unit")
@login_required
def unit_update(request, pk): return model_form_view(request, Unit, UnitForm, "properties/unit_form.html", "property_list", pk, "Unit")
@login_required
def unit_delete(request, pk): return model_delete_view(request, Unit, "property_list", pk, "Unit")
