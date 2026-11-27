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
    def __init__(self, *args, property_obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        if property_obj is not None:
            self.fields["building"].queryset = Building.objects.filter(
                property=property_obj
            )

    class Meta:
        model = Unit
        exclude = ("created_at", "updated_at")
