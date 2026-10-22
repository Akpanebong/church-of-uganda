from django import forms
from .models import MaintenanceRequest

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        exclude = ("created_at", "updated_at")
        widgets = {"scheduled_date": forms.DateInput(attrs={"type": "date"}), "completed_date": forms.DateInput(attrs={"type": "date"})}
