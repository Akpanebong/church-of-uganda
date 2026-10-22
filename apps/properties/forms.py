from django import forms
from .models import Property, Building, Unit

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ("created_at", "updated_at")
        widgets = {
            "acquisition_date": forms.DateInput(attrs={"class": "date", 'type': 'date'}),
            "address": forms.Textarea(attrs={"class": "form-control", 'type': 'text', 'rows': 1}),
            "description": forms.Textarea(attrs={"class": "form-control", 'type': 'text', 'rows': 1}),
        }

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        exclude = ("created_at", "updated_at")

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        exclude = ("created_at", "updated_at")
