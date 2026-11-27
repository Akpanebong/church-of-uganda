from django import forms
from .models import Tenant, TenantUnit

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ("created_at", "updated_at", "tenant_id")
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
        }


#OCCUPANCY
class TenantUnitForm(forms.ModelForm):
    class Meta:
        model = TenantUnit
        exclude = ("created_at", "updated_at")
        widgets = {
            "move_in": forms.DateInput(attrs={"class": "date", 'type': 'date'}),
            "move_out": forms.DateInput(attrs={"class": "date", 'type': "date"}),
        }
